﻿# CougarTechSolutionsProject rest api endpoints 
# Admin credentials are hardcoded (admin/password)
1. Users (Customers & Admin)
GET /user/all → Returns all users (admin only).
GET /user/?id=USER_ID → Get details of a specific user.
POST /user → Register a new user.
PUT /user → Update a user’s profile.
DELETE /user → Delete a user account.
2. Baseball Cards
GET /card/all → Get all available baseball cards.
GET /card/?id=CARD_ID → Get details of a specific card.
POST /card → Admin adds a new baseball card.
PUT /card → Admin updates card info.
DELETE /card → Admin deletes a card.
3. Shopping Cart
POST /cart → Create a cart for a user.
GET /cart?user_id=USER_ID → View user’s cart.
POST /cart/item → Add a card to the cart.
PUT /cart/item → Update item quantity.
DELETE /cart/item → Remove an item from the cart.
DELETE /cart → Delete the entire cart.
4. Checkout (Interest Form)
POST /checkout → Sends a confirmation email to the admin & customer.
