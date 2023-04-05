CREATE EXTENSION IF NOT EXISTS aws_lambda CASCADE;
CREATE OR REPLACE FUNCTION respond_with_lambda()
  RETURNS TRIGGER
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
    IF cardinality(TG_ARGV)!=2 THEN
      RAISE EXCEPTION 'Expected 2 parameters to respond_with_lambda function but got %', cardinality(TG_ARGV);
   ELSEIF TG_ARGV[0]='' THEN
      RAISE EXCEPTION 'Lambda name is empty';
   ELSEIF TG_ARGV[1]='' THEN
      RAISE EXCEPTION 'Lambda region is empty';
   ELSE
       PERFORM * FROM aws_lambda.invoke(aws_commons.create_lambda_function_arn(TG_ARGV[0], TG_ARGV[1]),
                               CONCAT('{"zpid": "', NEW.zpid,'", 
									  "price": "', NEW.price,'",
									  "area": "', NEW.area,'",
									  "lat": "', NEW.lat,'",
									  "long": "', NEW.long,'",
									  "statustype": "', NEW.statustype,'",
									  "zestimate": "', NEW.zestimate,'",		
									  "rentzestimate": "', NEW.rentzestimate,'",
									  "taxassessedvalue": "', NEW.taxassessedvalue,'",
									  "web_link": "', NEW.web_link,'",
									  "address": "', NEW.address,'"
									  }')::json,'Event');
        RETURN NEW;
    END IF;
END
$$;
DROP TRIGGER IF EXISTS new_listing_trigger ON zillow_data;
CREATE TRIGGER new_listing_trigger
  AFTER INSERT ON zillow_data
  FOR EACH ROW
  EXECUTE PROCEDURE respond_with_lambda("on_new_zillow_listing","us-east-1");
  
 
INSERT INTO zillow_data(zpid, price, area, lat, long, statustype, zestimate, rentzestimate, taxassessedvalue)
VALUES (129, 555666, 500, 500000, 500000, 'FOR_SALE', 500000, 5000, 400000);

ALTER TABLE zillow_data ADD COLUMN web_link VARCHAR;

ALTER TABLE zillow_data ADD COLUMN address VARCHAR;

ALTER TABLE zillow_data ADD COLUMN time_to_gov_center INTEGER;