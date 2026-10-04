#!/usr/bin/env python3
"""Real manager and local Git fixtures; never touch personal skill targets."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import installed_skills as adapter


class InstalledSkills(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='installed-skills-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.checkout, self.remote = self.root/'canonical', self.root/'remote.git'
        self.git = str(Path(shutil.which('git')).resolve())
        self.command('init','--bare','--initial-branch=main',str(self.remote))
        self.command('clone',str(self.remote),str(self.checkout))
        self.command('-C',str(self.checkout),'config','user.name','Synthetic fixture')
        self.command('-C',str(self.checkout),'config','user.email','fixture@example.invalid')
        (self.checkout/'scripts').mkdir()
        for name in ['manage-skills.sh','validate-skills.py']:
            shutil.copy2(ROOT/'scripts'/name,self.checkout/'scripts'/name)
        shutil.copytree(ROOT/'tests/fixtures/valid-skill',self.checkout/'skills/valid-skill')
        (self.checkout/'personal.txt').write_text('baseline\n')
        self.command('-C',str(self.checkout),'add','.')
        self.command('-C',str(self.checkout),'commit','-m','baseline')
        self.previous=self.command('-C',str(self.checkout),'rev-parse','HEAD').strip()
        self.command('-C',str(self.checkout),'push','origin','main')
        self.source=self.root/'candidate'
        self.command('clone',str(self.remote),str(self.source))
        self.command('-C',str(self.source),'config','user.name','Synthetic fixture')
        self.command('-C',str(self.source),'config','user.email','fixture@example.invalid')
        path=self.source/'skills/valid-skill/SKILL.md'
        path.write_text(path.read_text()+'\nPreserve the supplied facts.\n')
        self.publish()
        links=[]
        for agent in ['codex','claude']:
            dest=self.root/agent
            dest.mkdir()
            link=dest/'valid-skill';link.symlink_to(self.checkout/'skills/valid-skill')
            links.append({'agent':agent,'skill':'valid-skill','path':str(link)})
        self.evidence=self.root/'evidence';self.evidence.mkdir(mode=0o700)
        path=os.pathsep.join([str(Path(sys.executable).parent),'/usr/bin','/bin'])
        tools={str(Path(shutil.which(name,path=path)).resolve()) for name in adapter.TOOLS}
        tools.update(str(self.checkout/'scripts'/name) for name in ['manage-skills.sh','validate-skills.py'])
        self.config={'schemaVersion':1,'repository':'jimmie-potts/agent-skills','owner':'fixture',
                     'checkout':str(self.checkout),'stateDirectory':str(self.root/'state'),'evidenceRoot':str(self.evidence),
                     'git':self.git,'path':path,'allowedPaths':['skills/valid-skill/SKILL.md'],'protectedPaths':[],
                     'requiredSkills':['valid-skill'],'links':links,
                     'files':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in tools}}
        self.config_path=self.root/'config.json';self.save_config()
        self.counter=0
        remote=patch.object(adapter,'REMOTE_URLS',{str(self.remote)})
        remote.start();self.addCleanup(remote.stop)

    def command(self,*args):
        return subprocess.check_output([self.git,*args],text=True,stderr=subprocess.DEVNULL)

    def publish(self):
        self.command('-C',str(self.source),'add','.')
        self.command('-C',str(self.source),'commit','-m','selected change')
        self.target=self.command('-C',str(self.source),'rev-parse','HEAD').strip()
        self.command('-C',str(self.source),'push','origin','main')

    def save_config(self):
        self.config_path.write_text(json.dumps(self.config));self.config_path.chmod(0o600)

    def request(self,operation='install'):
        self.counter+=1
        evidence=self.evidence/str(self.counter);evidence.mkdir(mode=0o700)
        request={'schemaVersion':1,'operation':operation,'repository':'jimmie-potts/agent-skills','issue':140,
                 'merge':self.target,'owner':'fixture','deadline':time.time()+90,'evidenceDirectory':str(evidence)}
        return request

    def run_adapter(self,operation='install'):
        return adapter.run(self.config_path,self.request(operation))

    def test_existing_skill_update_uses_real_manager_and_reads_both_loading_paths(self):
        (self.checkout/'personal.txt').write_bytes(b'preserved owner work\x00\xff')
        result=self.run_adapter()
        self.assertEqual(result['status'],'installed',result)
        self.assertEqual(result['readbackKind'],'installed-files')
        self.assertNotIn('health',result)
        receipt=Path(result['receipt']['path'])
        self.assertEqual(hashlib.sha256(receipt.read_bytes()).hexdigest(),result['receipt']['sha256'])
        proof=json.loads(receipt.read_text())
        self.assertEqual(proof['schemaVersion'],'installed-files/1.0')
        self.assertEqual(proof['readback']['revision'],self.target)
        self.assertEqual(proof['readback']['links'],proof['plan']['links'])
        self.assertEqual(set(proof['readback']['managerStatus']),{'codex','claude'})
        self.assertEqual((self.checkout/'personal.txt').read_bytes(),b'preserved owner work\x00\xff')
        for link in self.config['links']:
            self.assertEqual((Path(link['path'])/'SKILL.md').read_bytes(),(self.source/'skills/valid-skill/SKILL.md').read_bytes())

    def test_affected_skill_dirty_even_when_changed_file_itself_is_clean(self):
        path=self.checkout/'skills/valid-skill/owner-note.txt';path.write_text('preserve owner note')
        result=self.run_adapter()
        self.assertEqual((result['status'],result['effects'],result['reason']),('blocked','none','affected-skill-dirty'))
        self.assertEqual(path.read_text(),'preserve owner note')
        self.assertEqual(self.command('-C',str(self.checkout),'rev-parse','HEAD').strip(),self.previous)

    def test_missing_or_foreign_required_links_are_never_created_or_replaced(self):
        path=Path(self.config['links'][0]['path']);path.unlink()
        self.assertEqual(self.run_adapter()['status'],'blocked')
        self.assertFalse(path.exists())
        path.symlink_to(self.source/'skills/valid-skill')
        result=self.run_adapter()
        self.assertEqual((result['status'],result['effects']),('blocked','none'))
        self.assertEqual(path.resolve(),self.source/'skills/valid-skill')

    def test_new_skill_requires_discovery_even_when_allowlisted(self):
        path=self.source/'skills/new-skill';path.mkdir()
        (path/'SKILL.md').write_text((self.source/'skills/valid-skill/SKILL.md').read_text().replace('valid-skill','new-skill'))
        self.publish();self.config['allowedPaths'].append('skills/new-skill/SKILL.md');self.save_config()
        result=self.run_adapter()
        self.assertEqual((result['status'],result['reason']),('blocked','new-renamed-or-retired-skill-needs-discovery'))

    def test_retirement_cannot_fast_forward_or_unlink(self):
        self.command('-C',str(self.source),'rm','skills/valid-skill/SKILL.md');self.publish()
        result=self.run_adapter()
        self.assertEqual(result['reason'],'new-renamed-or-retired-skill-needs-discovery')
        self.assertTrue(Path(self.config['links'][0]['path']).is_symlink())

    def test_unreviewed_bundle_and_protected_machinery_refuse(self):
        (self.source/'personal.txt').write_text('uncovered setting')
        self.publish()
        result=self.run_adapter()
        self.assertEqual((result['status'],result['reason']),('blocked','unreviewed-or-protected-bundle'))
        self.config['allowedPaths'].append('personal.txt');self.save_config()
        self.assertEqual(self.run_adapter()['status'],'blocked')
        for path in ['README.md','AGENTS.md','scripts/manage-skills.sh','skills/review-work/SKILL.md']:
            self.assertTrue(adapter.protected(self.config,path))

    def test_lost_fast_forward_response_reconciles_without_repeating_mutation(self):
        real_git=adapter.git;mutations=[]
        def lost(config,args,deadline,**kwargs):
            value=real_git(config,args,deadline,**kwargs)
            if kwargs.get('mutation'):
                mutations.append(args);raise OSError('synthetic lost response')
            return value
        with patch.object(adapter,'git',side_effect=lost):
            self.assertEqual(self.run_adapter()['status'],'uncertain')
        self.assertEqual(self.run_adapter()['reason'],'read-only-reconciliation-required')
        def read_only(config,args,deadline,**kwargs):
            self.assertNotIn(args[0],{'fetch','merge','reset','checkout'})
            return real_git(config,args,deadline,**kwargs)
        real_manager=adapter.manager
        def status_only(config,deadline,action,**kwargs):
            self.assertEqual(action,'status');return real_manager(config,deadline,action,**kwargs)
        with patch.object(adapter,'git',side_effect=read_only),patch.object(adapter,'manager',side_effect=status_only):
            result=self.run_adapter('reconcile')
        self.assertEqual(result['status'],'installed',result)
        self.assertEqual(len(mutations),1)

    def test_interruption_before_merge_never_retries(self):
        real_git=adapter.git
        def stop(config,args,deadline,**kwargs):
            if kwargs.get('mutation'):raise OSError('synthetic interruption')
            return real_git(config,args,deadline,**kwargs)
        with patch.object(adapter,'git',side_effect=stop):
            self.assertEqual(self.run_adapter()['status'],'uncertain')
        self.assertEqual(self.run_adapter('reconcile')['status'],'uncertain')
        self.assertEqual(self.run_adapter()['status'],'uncertain')

    def test_modified_trusted_manager_is_not_executed(self):
        path=self.checkout/'scripts/manage-skills.sh';path.write_text('#!/bin/bash\nexit 0\n')
        result=self.run_adapter()
        self.assertEqual(result['reason'],'trusted-input-changed')
        self.assertEqual(self.command('-C',str(self.checkout),'rev-parse','HEAD').strip(),self.previous)

    def test_saved_receipt_does_not_hide_later_loading_corruption(self):
        self.assertEqual(self.run_adapter()['status'],'installed')
        (self.checkout/'skills/valid-skill/SKILL.md').write_text('unverified replacement')
        result=self.run_adapter('reconcile')
        self.assertNotEqual(result['status'],'installed')
        self.assertEqual(result['reason'],'installed-files-incomplete')

    def test_hidden_dirty_change_after_plan_refuses_before_durable_intent(self):
        real_prepare=adapter.prepare;path=self.checkout/'skills/valid-skill/SKILL.md'
        def changed(*args):
            plan=real_prepare(*args)
            self.command('-C',str(self.checkout),'update-index','--assume-unchanged','skills/valid-skill/SKILL.md')
            path.write_text('owner edit hidden from status')
            return plan
        with patch.object(adapter,'prepare',side_effect=changed):result=self.run_adapter()
        self.assertEqual((result['status'],result['effects']),('blocked','none'))
        self.assertFalse((self.root/'state/active.json').exists())

    def test_git_attributes_cannot_execute_a_filter(self):
        marker=self.root/'filter-ran'
        self.command('-C',str(self.checkout),'config','filter.fixture.clean','touch '+str(marker))
        (self.checkout/'.git/info/attributes').write_text('skills/*/* filter=fixture\n')
        self.assertEqual(self.run_adapter()['status'],'blocked')
        self.assertFalse(marker.exists())

    def test_extra_installed_target_cannot_be_omitted_from_configuration(self):
        other=self.checkout/'skills/other-skill';other.mkdir()
        (other/'SKILL.md').write_text((self.checkout/'skills/valid-skill/SKILL.md').read_text().replace('valid-skill','other-skill'))
        other_link=self.root/'claude/other-skill';other_link.symlink_to(other)
        self.config['links'][1]={'agent':'claude','skill':'other-skill','path':str(other_link)}
        self.config['requiredSkills'].append('other-skill');self.save_config()
        result=self.run_adapter()
        self.assertEqual((result['status'],result['effects']),('blocked','none'))
        self.assertEqual(self.command('-C',str(self.checkout),'rev-parse','HEAD').strip(),self.previous)

    def test_real_cli_returns_the_installed_files_contract(self):
        tools=self.root/'tools';tools.mkdir()
        tool=tools/'git'
        tool.write_text('#!'+sys.executable+'\nimport os,sys\n'
                        "if sys.argv[-3:] == ['remote','get-url','origin']:\n print('https://github.com/jimmie-potts/agent-skills.git')\n"
                        'else:\n os.execv('+repr(self.git)+', ['+repr(self.git)+', *sys.argv[1:]])\n')
        tool.chmod(0o700)
        self.config.update(git=str(tool),path=str(tools)+os.pathsep+self.config['path'])
        self.config['files'][str(tool)]=hashlib.sha256(tool.read_bytes()).hexdigest();self.save_config()
        result=subprocess.check_output([sys.executable,str(Path(adapter.__file__)),'--config',str(self.config_path)],
                                       input=json.dumps(self.request()),text=True)
        response=json.loads(result)
        self.assertEqual(response['status'],'installed',response)
        self.assertEqual(response['installedRevision'],self.target)


if __name__=='__main__': unittest.main()
