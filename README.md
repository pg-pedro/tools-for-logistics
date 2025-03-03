 

# Tools for Logistics

## Intro

_Tools for Logistics_ is a web app. The Swiss army knife of the logistics engineer.
It is a collection of generic tools to create quick insights on customers data.

It provides a user-friendly interface to upload data, preprocess and merge datasets, and generate various reports and dashboards.
Current phase is __prototype__, meant to show to logistics engineers how they could streamline their work with such tools.

A working version of the app can be found [here](https://tools-for-logistics.streamlit.app/).

## Key Features
1. **Upload Data**: Supports CSV, XLS, and XLSX file formats up to 2GB.
2. **Merge and Preprocess**: Convert data types, drop unnecessary columns, and set datetime indexes.
3. **Select Report**: Choose from various report types tailored for logistics analysis.
4. **Set Parameters and Create Dashboards**: Customize report parameters and generate interactive dashboards.
5. **Download Report Data**: Export the processed data and reports for further analysis or sharing.

---

# Tasks

## Outbound

Tools currently avalable:

### ABC Classification

ABC classification is a ranking system for identifying and grouping items in terms of how useful they are for achieving business goals.
The system requires grouping things into three categories:

A - extremely important

B - moderately important

C - relatively unimportant

ABC classification is associated with the 80/20 rule, a business metric that proposes 80% of the outcomes are determined by 20% of the inputs.  The goal of ABC classification is to provide a way for a business to identify that valuable 20% so that segment can be controlled most closely.  Once the A’s, B’s and C’s have been identified, each category can be handled in a different way, with more attention being devoted to category A, less to B, and even less to C.

<!-- [Source](https://www.techtarget.com/searcherp/definition/ABC-classification) -->

![Abc Classification](/assets/images/abc-class.PNG "ABC Classification - Picklines")
### Orderline Pattern

![Orderline Pattern](/assets/images/orderline-pattern.png "Orderline Pattern")

### Outbound Overview

General outbound info, such as number of daily orderlines. 
Weekday box plot and largest daily orderline heatmap.

![Daily Orderlines](/assets/images/orderline-pattern.png "Daily Orderlines")

---

## Inbound

TODO

---

## Storage

TODO

---


## Returns

TODO

---