## Dimension tables for Sample SD module 

## Fact tables 
### Sale fact talble 

| Column         | Description                       | Source SAP Table |
| -------------- | --------------------------------- | ---------------- |
| `billing_doc`  | Billing Document Number (`VBELN`) | `VBRP`           |
| `item_no`      | Billing Item Number (`POSNR`)     | `VBRP`           |
| `billing_date` | Billing Date (`FKDAT`)            | `VBRK`           |
| `customer_id`  | Sold-to Party (`KUNAG`)           | `VBRK`           |
| `payer_id`     | payer (`KUNRG`)                   | `VBRK`           |
| `material_id`  | Material Number (`MATNR`)         | `VBRP`           |
| `sales_org`    | Sales Organization (`VKORG`)      | `VBRK` / `KNVV`  |
| `sales_qty`    | Billing Quantity (`FKIMG`)        | `VBRP`           |
| `net_value`    | Net Value (`NETWR`)               | `VBRP`           |
| `currency`     | Currency (`WAERK`)                | `VBRK`           |
| `plant`        | Plant (`WERKS`)                   | `VBRP`           |

## Dimension table 
### DIM material tables 

| Column           | Description               | Source |
| ---------------- | ------------------------- | ------ |
| `material_id`    | Material Number (`MATNR`) | `MARA` |
| `material_desc`  | Description               | `MAKT` |
| `material_group` | Material Group            | `MARA` |

### Customer 

| Column          | Description               | Source |
| --------------- | ------------------------- | ------ |
| `customer_id`   | Customer Number (`KUNNR`) | `KNA1` |
| `customer_name` | Name                      | `KNA1` |
| `city`          | City                      | `ADRC` |
| `region`        | Region                    | `ADRC` |
| `country`       | Country                   | `KNA1` |

### Sale organization 

| Column                 | Description             | Source |
| ---------------------- | ----------------------- | ------ |
| `sales_org`            | Sales Organization Code | `KNVV` |
| `distribution_channel` | Dist. Channel           | `KNVV` |
| `division`             | Division                | `KNVV` |

### Date table 

| Column      | Description   |
| ----------- | ------------- |
| `date_key`  | Surrogate Key |
| `full_date` | Date          |
| `month`     | Month         |
| `quarter`   | Quarter       |
| `year`      | Year          |

## FICO fact table 

| Column         | Source Table | Description            |
| -------------- | ------------ | ---------------------- |
| `document_no`  | BKPF-BELNR   | Accounting doc number  |
| `line_item`    | BSEG-BUZEI   | Line item number       |
| `customer_id`  | BSEG-KUNNR   | Linked to KNA1         |
| `gl_account`   | BSEG-HKONT   | General Ledger account |
| `amount`       | BSEG-DMBTR   | Line item amount       |
| `currency`     | BKPF-WAERS   | Currency               |
| `posting_date` | BKPF-BUDAT   | Date of posting        |
| `fiscal_year`  | BKPF-GJAHR   | Fiscal year            |

### Dim 
### dim material 

| Column              | Description                        | Source Table |
| ------------------- | ---------------------------------- | ------------ |
| `material_id`       | Material Number (Product Code)     | `MARA-MATNR` |
| `material_desc`     | Material Description               | `MAKT-MAKTX` |
| `material_group`    | Material Group (Product Category)  | `MARA-MATKL` |
| `base_uom`          | Base Unit of Measure               | `MARA-MEINS` |
| `product_hierarchy` | Product Hierarchy (e.g., 0001.003) | `MARA-PRDHA` |

### dim gl_account 
| Column            | Description                              | Source Table           |
| ----------------- | ---------------------------------------- | ---------------------- |
| `gl_account`      | GL Account Number                        | `SKA1-SAKNR`           |
| `gl_account_name` | GL Account Name (Long Text)              | `SKAT-TXT50`           |
| `account_group`   | Grouping for Chart of Accounts           | `SKA1-KTOPL`           |
| `account_type`    | Type of Account (Asset, Liability, etc.) | `SKA1-BILKT` or config |
| `valid_from`      | Valid From Date                          | (derived)              |



## COPA fact table 

| Column          | Description                         | Source (CE1xxxx)                 |
| --------------- | ----------------------------------- | -------------------------------- |
| `record_type`   | Type of record (actual, plan, etc.) | `PA_TYPE`                        |
| `customer_id`   | Customer                            | `KNDNR`                          |
| `material_id`   | Product                             | `ARTNR`                          |
| `billing_doc`   | Billing document                    | `BELNR`                          |
| `sales_org`     | Sales org                           | `VKORG`                          |
| `profit_center` | Profit center                       | `PRCTR`                          |
| `cost_element`  | Cost/revenue account                | `PAOBJNR` / `SARTN`              |
| `value_type`    | Type of value (revenue, cost)       | `VRGAR`                          |
| `amount`        | Revenue or cost amount              | `WERT`                           |
| `currency`      | Currency                            | `WAERS`                          |
| `fiscal_year`   | Year                                | `GJAHR`                          |
| `posting_date`  | Date                                | Derived from `PERIO` and `GJAHR` |

### Share table 
dim_customer (from KNA1)

dim_date (posting/billing)

dim_gl_account (from SKA1 or COA)

dim_material (for sales)

dim_company_code (BUKRS)

### Extented star schema  
https://www.guru99.com/all-about-classical-extended-star-sch

## SID table 