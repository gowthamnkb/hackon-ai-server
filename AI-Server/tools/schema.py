DB_SCHEMA = """
Tables:
1. merchants (id TEXT PRIMARY KEY, name TEXT, status TEXT)
2. users (id TEXT PRIMARY KEY, name TEXT, merchant_id TEXT, partner_customer_id TEXT, contact TEXT, ignore records with parent_user_id is equal to "")
3. wallets (id TEXT PRIMARY KEY, user_id TEXT, account_id TEXT)
4. accounts (id TEXT PRIMARY KEY, program_id TEXT, user_id TEXT, balance_id TEXT)
5. balances (id TEXT PRIMARY KEY, balance INT is current balance)
6. transactions (id TEXT PRIMARY KEY, account_id TEXT, credit INT, debit INT, balance INT is balance after this transaction,
    created_at INT unix timestamp)
7. recharges(id TEXT PRIMARY KEY, account_id TEXT, amount INT, status TEXT, created_at INT unix timestamp)
8. payments(id TEXT PRIMARY KEY, account_id TEXT, amount INT, status TEXT, created_at INT unix timestamp)
8. refunds(id TEXT PRIMARY KEY, account_id TEXT, amount INT, status TEXT, created_at INT unix timestamp)

Relationships:
- accounts.user_id → users.id (One user can have multiple accounts)
- accounts.balance_id → balances.id (One account can have one balance)
- wallets.account_id → accounts.id (One wallet can have one account)
- transactions.account_id → accounts.id (One account can have many transactions)
- recharges.account_id → accounts.id (One account can have many recharges)
- payments.account_id → accounts.id (One account can have many payments)
- refunds.account_id → accounts.id (One account can have many refunds)
- transactions.entity_type = 'recharge' and transactions.entity_id → recharges.id (One recharge can have one transaction)
- transactions.entity_type = 'payment' and transactions.entity_id → payments.id (One payment can have one transaction)
- transactions.entity_type = 'refund' and transactions.entity_id → refunds.id (One refund can have one transaction)

"""