Este módulo depende de:

* `l10n_br_fiscal_dfe`
* `l10n_br_nfse`
* `l10n_br_fiscal_certificate`
* `queue_job` (exigido pelo motor de DF-e)

Bibliotecas Python: `nfelib` (>= 3.3.0) consulta o lote, os eventos no ADN e a nota autorizada na Sefin Nacional. `requests` e `cryptography` são usadas pelo cliente da biblioteca para o mTLS.

A empresa precisa de um certificado e-CNPJ A1 válido, o mesmo já utilizado pela localização fiscal.
