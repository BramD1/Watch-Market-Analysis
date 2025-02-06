CREATE TABLE table_m3 (
    "Brand" VARCHAR(50),                    -- The name of the brand
    "Movement" VARCHAR(50),                 -- The mechanism of the watch
    "Case material" VARCHAR(50),            -- Materials of the watch's case around the glass
    "Bracelet material" VARCHAR(50),        -- Materials of the watch's bracelet
    "Year of production" DECIMAL,           -- Years the watch is produced
    "Condition" VARCHAR(50),                -- Watches condition (New, Used, etc)
    "Scope of delivery" VARCHAR(50),        -- Packaging
    "Gender" VARCHAR(50),                   -- Which gender is suited to wear the watch
    "Price" DECIMAL,                        -- The value of the watch
    "Availability" VARCHAR(50),             -- Stock of the watches
    "Shape" VARCHAR(50),                    -- Shape of the watches (square or circle)
    "Face Area" DECIMAL,                    -- Face area of the watches
    "Water resistance" DECIMAL,             -- Water resistance of the watched
    "Crystal" VARCHAR(50),                  -- Glasses being used to protect the clock inside the watch
    "Dial" VARCHAR(50),                     -- Color of the watch
    "Bracelet color" VARCHAR(50),           -- Color of the watch's bracelet
    "Clasp" VARCHAR(50),                    -- Type of clasp for the bracelet
    "Watches Sold by the Seller" DECIMAL,   -- number of watches sold by the seller
    "Active listing of the seller" DECIMAL, -- number of watches the seller hasn't sold
    "Fast Shipper" INT,                     -- if the shipment is fast
    "Trusted Seller" INT,                   -- if the seller is trusted
    "Punctuality" INT,                      -- if the shipment is punctual
    "Seller Reviews" DECIMAL                -- the number of reviews the seller had
)