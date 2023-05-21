# Chezuba : Software Developer Assignment

## Models for Topkart Lightning Deals API
    1) LightningDeal
    2) Order

## Endpoints for Topkart Lightning Deals API

### Admin Actions

#### Create a Lightning Deal
    Endpoint: /lightning_deals
    Method: POST
    Description: Creates a new lightning deal.

#### Update a Lightning Deal

    Endpoint: /lightning_deals/{deal_id}
    Method: PUT
    Description: Updates an existing lightning deal.

#### Approve the order

    Endpoint: /orders/{order_id}
    Method: PUT
    Description: Approves the order.


### Customer Actions

#### Get Available Deals

    Endpoint: /lightning_deals
    Method: GET
    Description: Retrieves the list of available unexpired lightning deals.

#### Place an Order

    Endpoint: /orders
    Method: POST
    Description: Places an order for a lightning deal.

#### Check Order Status

    Endpoint: /orders/{order_id}
    Method: GET
    Description: Retrieves the status of an order.
