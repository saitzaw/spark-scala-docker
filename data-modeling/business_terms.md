# Translation of Techanical terms to business terms 
- SAP tech term to business term 

## MM (Materials Management) tables 

| SAP Table | Business Term / Description | Common Usage                                 |
| --------- | --------------------------- | -------------------------------------------- |
| **MARA**  | General Material Data       | Stores material master data                  |
| **MAKT**  | Material Descriptions       | Material names in different languages        |
| **MBEW**  | Material Valuation          | Inventory valuation (price, currency, etc.)  |
| **EKPO**  | Purchase Order Item         | Line items for purchase orders               |
| **EKKO**  | Purchase Order Header       | Header-level info for purchase orders        |
| **EBAN**  | Purchase Requisition        | Request for material purchases               |
| **MKPF**  | Material Document Header    | Goods movement header                        |
| **MSEG**  | Material Document Items     | Line items for goods movement (GR, GI, etc.) |

## SD (Sales and Distributions) tables 

| SAP Table | Business Term / Description | Common Usage                                    |
| --------- | --------------------------- | ----------------------------------------------- |
| **VBAK**  | Sales Document Header       | Sales order header info                         |
| **VBAP**  | Sales Document Items        | Sales order item info                           |
| **VBEP**  | Schedule Lines              | Delivery schedule lines                         |
| **VBRK**  | Billing Document Header     | Billing header (invoice, credit memo, etc.)     |
| **VBRP**  | Billing Document Item       | Billing line items                              |
| **VBFA**  | Document Flow               | Tracks document relationships (sales → billing) |
| **LIKP**  | Delivery Header             | Delivery document header                        |
| **LIPS**  | Delivery Items              | Line items for delivery                         |
| **KNA1**  | General Customer Master     | Basic customer data                             |


## FICO tables 

| SAP Table | Business Term / Description            | Common Usage                              |
| --------- | -------------------------------------- | ----------------------------------------- |
| **BKPF**  | Accounting Document Header             | Header for financial postings             |
| **BSEG**  | Accounting Document Segment            | Line items for financial documents        |
| **SKA1**  | G/L Account Master (Chart of Accounts) | Chart-level account info                  |
| **SKB1**  | G/L Account Master (Company Code)      | Company-specific account info             |
| **LFA1**  | Vendor Master (General)                | Vendor info across all companies          |
| **BSID**  | Customer Open Items                    | Receivables                               |
| **BSAD**  | Customer Cleared Items                 | Settled receivables                       |
| **BSAK**  | Vendor Cleared Items                   | Settled payables                          |
| **BSIK**  | Vendor Open Items                      | Payables                                  |
| **T030**  | Account Determination                  | Used for automatic postings (e.g., GR/IR) |

## MW (warehouse management) taables 

| SAP Table | Business Term / Description   | Common Usage                               |
| --------- | ----------------------------- | ------------------------------------------ |
| **LAGP**  | Storage Bin Master            | Details of bins in a warehouse             |
| **LQUA**  | Quants in Storage Bins        | Quantities of stock in bins                |
| **LTAP**  | Transfer Order Items          | Details of stock movement within warehouse |
| **LTAK**  | Transfer Order Header         | Movement request document header           |
| **MLGN**  | Material Master: Warehouse    | Warehouse-specific data                    |
| **MLGT**  | Material Master: Storage Type | Data by storage type                       |



- Salesforce term to business term 