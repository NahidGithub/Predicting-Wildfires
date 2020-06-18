# Tables needed from MySQL

### _san_xcart_
* cust_kantar 
  - this is not changing so just a one time load
  - might make most sense to load customer_kantar
  - this data was a one time update of Kantar profiles and some other attributes about our customer base provided by the NBDU team
* List_Campaigns
* List_Entries
* List_Segments
* manual_transaction
* manual_transaction_partial
* order_fraud_history _::: future_
* order_fraud_history_rules _::: future_
* refund_items
* refund_request_log
* SAP_Ship_Details
* SAP_SKU_Sales
* SAP_Summary
* sap_approved
* xcart_categories
* xcart_cust_access
  - if we want to know who is marked DNM
* xcart_access_codes
  - related to cust_access
* xcart_discount_coupons
* xcart_discount_coupons_customers
* xcart_states
  - dont need to sync but should have a lookup table for this info in Snowflake
* zipcode_lookup
  - dont need to sync but should have a lookup table for this info in Snowflake
* xcart_subscription_customers_alt
* xcart_subscription_changes
* xcart_subscription_renewals
* xcart_subscription_renewal_details





## Needed for TH/BH Only
### _san_xcart_
* Customer_Lifetime 
* Detail_Summary_base
* elistman_lists
* elistman_lists_prime_brand
* Order_Summary
* SKU_Summary
* xcart_ _::: tables_
  - I can pocure these more based on reporting needs.  We will still need a plan for when we need to quickly get a table synced since it is no longer just turning it on with FiveTran.


## Other Interesting Tables
### _san_xcart_
* Prod_Reorder_Cycle
  - this is the table that shows the reorder compliance
* prospect_dnc
  - there are three tables that start with this string. They were created to use as suppressions when we rent lists.  If we are no longer using coops then these most likely will not be needed right now
* SKU_Vol_Price
  - If we can find the code for this agg table it might unlock the Volume Price column for OIM
* SS_Data
  - smarty streets data; if we ever want to see how many addresses or what addresses are being corrected
* Survey1_Data
* Survey2_Data
* Survey3_Data
* Survey4_Data
* Survey_Questions
