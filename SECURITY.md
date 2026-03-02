# Security Policy

## Scope

This project handles personal and family profile data. Treat all real datasets as sensitive.

## Safe Usage

- Keep encrypted data in local `*.enc` files only.
- Do not commit `.env` or any real profile export.
- Use strong passwords for local encrypted storage.
- Rotate credentials if you suspect exposure.

## Data Exposure Response

If sensitive data is committed by mistake:

1. Rotate affected secrets immediately.
2. Remove sensitive files from git history.
3. Re-encrypt local data with a new password.
4. Open a private incident note documenting impact and remediation.

## Reporting

Report security issues privately to repository maintainers before public disclosure.
