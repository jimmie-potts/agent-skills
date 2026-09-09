// Render the inert report example and hostile labels without network access.
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

async function main() {
  const output = process.env.ARCHITECTURE_REPORT_OUTPUT
    || await fs.mkdtemp(path.join(os.tmpdir(), 'architecture-report-'));
  await fs.mkdir(output, { recursive: true });
  const source = path.join(__dirname, '../skills/improve-codebase-architecture/assets/report.html');
  const example = await fs.readFile(source, 'utf8');
  const hostile = '</text><script>alert("source")</script><svg onload="alert(1)">& filename';
  const escaped = hostile.replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;');
  const report = example.replace('</footer>', '</footer>\n<p id="hostile-label">' + escaped + '</p>');
  const reportPath = path.join(output, 'report.html');
  await fs.writeFile(reportPath, report);
  const executablePath = process.env.ARCHITECTURE_REPORT_CHROMIUM;
  const browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
  try {
    const context = await browser.newContext({ offline: true });
    const page = await context.newPage();
    const requests = [], errors = [], dialogs = [], results = [];
    page.on('request', request => {
      if (/^https?:/i.test(request.url())) requests.push(request.url());
    });
    page.on('pageerror', error => errors.push(error.message));
    page.on('dialog', async dialog => { dialogs.push(dialog.message()); await dialog.dismiss(); });
    for (const width of [1200, 390]) {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(pathToFileURL(reportPath).href);
      const state = await page.evaluate(() => ({
        viewport: innerWidth,
        width: document.documentElement.scrollWidth,
        active: document.querySelectorAll('script,iframe,object,embed,foreignObject,[onload],[onclick]').length,
        figures: document.querySelectorAll('figure').length,
        hostile: document.getElementById('hostile-label').textContent,
        clipped: [...document.querySelectorAll('svg text')].filter(element => {
          const box = element.getBBox(), view = element.ownerSVGElement.viewBox.baseVal;
          return box.x < 0 || box.y < 0 || box.x + box.width > view.width || box.y + box.height > view.height;
        }).map(element => element.textContent),
        columns: getComputedStyle(document.querySelector('.figures')).gridTemplateColumns.split(' ').length,
      }));
      assert.ok(state.width <= width, 'Report overflows viewport');
      assert.equal(state.active, 0, 'Active elements or handlers appeared');
      assert.equal(state.figures, 2);
      assert.equal(state.hostile, hostile, 'Source label did not remain literal text');
      assert.deepEqual(state.clipped, [], 'Diagram text is clipped');
      assert.equal(state.columns, width === 390 ? 1 : 2);
      await page.screenshot({ path: path.join(output, `report-${width}.png`), fullPage: true });
      results.push(state);
    }
    assert.deepEqual(requests, [], 'Report attempted network access');
    assert.deepEqual(errors, [], 'Report raised browser errors');
    assert.deepEqual(dialogs, [], 'Source content triggered a dialog');
    const receipt = { results, requests, errors, dialogs };
    await fs.writeFile(path.join(output, 'result.json'), JSON.stringify(receipt, null, 2) + '\n');
    console.log(JSON.stringify(receipt, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
