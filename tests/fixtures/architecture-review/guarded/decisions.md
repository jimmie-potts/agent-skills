# Decision 4: Provider isolation

The integration team owns the Ledger adapter. Applications use LedgerUnavailable,
not provider exception types. A second provider is not planned. The seam exists
to isolate provider changes and error handling. Checksum tests protect a byte
protocol calculation that integration tests cannot diagnose precisely.
