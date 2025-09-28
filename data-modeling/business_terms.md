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

## source tables for SAP in this erp system 

| No. | File Name   | Description |
|-----|-------------|-------------|
| 1   | adr6.csv    | Addresses with organizational units. Contains address details related to organizational units like departments or branches. |
| 2   | adrc.csv    | General Address Data. Provides information about addresses, including details such as street, city, and postal codes. |
| 3   | adrct.csv   | Address Contact Information. Contains contact information linked to addresses, including phone numbers and email addresses. |
| 4   | adrt.csv    | Address Details. Includes detailed address data such as street addresses, city, and country codes. |
| 5   | ankt.csv    | Accounting Document Segment. Provides details on segments within accounting documents, including account numbers and amounts. |
| 6   | anla.csv    | Asset Master Data. Contains information about fixed assets, including asset identification and classification. |
| 7   | bkpf.csv    | Accounting Document Header. Contains headers of accounting documents, such as document numbers and fiscal year. |
| 8   | bseg.csv    | Accounting Document Segment. Details line items within accounting documents, including account details and amounts. |
| 9   | but000.csv  | Business Partners. Contains basic information about business partners, including IDs and names. |
| 10  | but020.csv  | Business Partner Addresses. Provides address details associated with business partners. |
| 11  | cepc.csv    | Customer Master Data - Central. Contains centralized data for customer master records. |
| 12  | cepct.csv   | Customer Master Data - Contact. Provides contact details associated with customer records. |
| 13  | csks.csv    | Cost Center Master Data. Contains data about cost centers within the organization. |
| 14  | cskt.csv    | Cost Center Texts. Provides text descriptions and labels for cost centers. |
| 15  | dd03l.csv   | Data Element Field Labels. Contains labels and descriptions for data fields in the SAP system. |
| 16  | ekbe.csv    | Purchase Order History. Details history of purchase orders, including quantities and values. |
| 17  | ekes.csv    | Purchasing Document History. Contains history of purchasing documents including changes and statuses. |
| 18  | eket.csv    | Purchase Order Item History. Details changes and statuses for individual purchase order items. |
| 19  | ekkn.csv    | Purchase Order Account Assignment. Provides account assignment details for purchase orders. |
| 20  | ekko.csv    | Purchasing Document Header. Contains headers for purchasing documents, such as order numbers and dates. |
| 21  | ekpo.csv    | Purchasing Document Item. Contains details about items within purchasing documents, including item numbers and quantities. |
| 22  | faglflexa.csv | General Ledger Flexibility Data. Contains flexible data related to general ledger accounts. |
| 23  | kna1.csv    | Customer Master Data. Provides detailed information about customers, including names and addresses. |
| 24  | konv.csv    | Conditions. Contains pricing conditions and agreements related to sales and purchasing documents. |
| 25  | lfa1.csv    | Vendor Master Data. Provides detailed information about vendors, including contact and banking details. |
| 26  | likp.csv    | Delivery Header Data. Contains headers for delivery documents, such as delivery numbers and dates. |
| 27  | lips.csv    | Delivery Item Data. Details items within delivery documents, including quantities and goods movement information. |
| 28  | makt.csv    | Material Descriptions. Provides descriptions for materials, including names and text. |
| 29  | mara.csv    | Material Master Data. Contains basic data for materials, such as material numbers and categories. |
| 30  | mard.csv    | Material Stock Data. Details stock levels for materials in different storage locations. |
| 31  | prps.csv    | Project Definition. Contains data related to project definitions, including project IDs and descriptions. |
| 32  | rbco.csv    | Vendor Bank Details. Provides bank account information for vendors. |
| 33  | rbkp.csv    | Invoice Document Header. Contains headers for invoice documents, including invoice numbers and dates. |
| 34  | rseg.csv    | Invoice Document Items. Details items within invoice documents, including amounts and descriptions. |
| 35  | setheadert.csv | Settlement Header Data. Contains header information for settlement documents. |
| 36  | setleaf.csv | Settlement Line Item Data. Provides details on line items within settlement documents. |
| 37  | setnode.csv | Settlement Node Data. Contains data on nodes related to settlements. |
| 38  | ska1.csv    | G/L Account Master Data. Contains information about general ledger accounts, including account numbers and descriptions. |
| 39  | skat.csv    | G/L Account Tax Data. Provides tax-related data for general ledger accounts. |
| 40  | t001.csv    | Company Codes. Contains data about company codes used within the SAP system. |
| 41  | t001w.csv   | Company Code Currency. Provides currency information for company codes. |
| 42  | t002.csv    | Currencies. Contains details about currencies used in the SAP system. |
| 43  | t005.csv    | Country Keys. Provides country codes and related information. |
| 44  | t005k.csv   | Country Key Mapping. Contains mappings between country codes and their descriptions. |
| 45  | t005s.csv   | Country Subdivision. Details sub-divisions within countries, such as states or provinces. |
| 46  | t005t.csv   | Country Key Texts. Contains textual descriptions of country keys. |
| 47  | t006.csv    | Units of Measure. Provides data on units of measure used in the SAP system. |
| 48  | t006a.csv   | Units of Measure (Additional). Contains additional information on units of measure. |
| 49  | t006t.csv   | Units of Measure Texts. Provides textual descriptions of units of measure. |
| 50  | t009.csv    | Currency Codes. Contains codes and descriptions for currencies. |
| 51  | t009b.csv   | Currency Codes (Additional). Provides additional information on currency codes. |
| 52  | t023.csv    | Tax Codes. Contains details about tax codes used in transactions. |
| 53  | t023t.csv   | Tax Code Texts. Provides textual descriptions for tax codes. |
| 54  | t134.csv    | Tax Codes for Tax on Sales/Purchases. Contains tax code details specific to sales and purchases. |
| 55  | t134t.csv   | Tax Code Texts for Sales/Purchases. Provides textual descriptions for sales and purchase tax codes. |
| 56  | t179.csv    | Tax Jurisdiction Codes. Contains codes related to tax jurisdictions. |
| 57  | t179t.csv   | Tax Jurisdiction Code Texts. Provides textual descriptions for tax jurisdiction codes. |
| 58  | t881.csv    | Tax Categories. Contains details on tax categories used within the system. |
| 59  | t881t.csv   | Tax Category Texts. Provides textual descriptions for tax categories. |
| 60  | tcurc.csv   | Currency Conversion Rates (Current). Contains current currency conversion rates. |
| 61  | tcurf.csv   | Currency Conversion Rates (Fixed). Provides fixed conversion rates for currencies. |
| 62  | tcurr.csv   | Currency Conversion Rates. Contains general currency conversion rates. |
| 63  | tcurt.csv   | Currency Conversion Rates (Table). Details conversion rates stored in table format. |
| 64  | tcurx.csv   | Currency Conversion Rates (Exchange). Provides exchange rates for currencies. |
| 65  | tka02.csv   | Cost Center Hierarchy. Contains hierarchical data for cost centers. |
| 66  | tvko.csv    | Sales Organization. Provides data about sales organizations within the system. |
| 67  | tvkot.csv   | Sales Organization Texts. Contains textual descriptions of sales organizations. |
| 68  | tvtw.csv    | Sales Office. Details information about sales offices. |
| 69  | tvtwt.csv   | Sales Office Texts. Provides textual descriptions of sales offices. |
| 70  | vbak.csv    | Sales Document Header. Contains headers for sales documents, such as sales order numbers and dates. |
| 71  | vbap.csv    | Sales Document Item. Details items within sales documents, including quantities and product details. |
| 72  | vbep.csv    | Sales Document Schedule. Provides schedule details for sales documents, including delivery dates. |
| 73  | vbfa.csv    | Sales Document Flow. Contains the flow of sales documents, tracking their status and changes. |
| 74  | vbpa.csv    | Sales Document Partners. Provides information on partners involved in sales documents. |
| 75  | vbrk.csv    | Billing Document Header. Contains headers for billing documents, including invoice numbers and dates. |
| 76  | vbrp.csv    | Billing Document Item. Details items within billing documents, including amounts and descriptions. |
| 77  | vbuk.csv    | Sales Document Status. Provides status information for sales documents, such as approval and processing status. |
| 78  | vbup.csv    | Sales Document Status (Update). Contains updated status information for sales documents. |


Note: get this table from the kaggle 



- Salesforce term to business term 