CREATE TABLE public.isone_auction (
                                      ftr_id bigserial NOT NULL,
                                      auction_name text NULL,
                                      customer_id int8 NULL,
                                      customer_name text NULL,
                                      source_location_id int8 NULL,
                                      source_location_name text NULL,
                                      source_location_type text NULL,
                                      sink_location_id int8 NULL,
                                      sink_location_name text NULL,
                                      sink_location_type text NULL,
                                      buy_sell text NULL,
                                      class_type text NULL,
                                      mw float8 NULL,
                                      price float8 NULL,
                                      auction_file text NULL,
                                      hour_price float8 NULL,
                                      CONSTRAINT isone_auction_pkey PRIMARY KEY (ftr_id)
);

CREATE TABLE public.isone_lmp (
                                  "date" text NULL,
                                  he int8 NULL,
                                  location_id int8 NOT NULL,
                                  location_name text NULL,
                                  location_type text NULL,
                                  lmp float8 NULL,
                                  energy float8 NULL,
                                  congestion float8 NULL,
                                  loss float8 NULL,
                                  datetime timestamp NOT NULL,
                                  CONSTRAINT isone_lmp_pk PRIMARY KEY (datetime, location_id)
);