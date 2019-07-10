--Start table creation
CREATE TABLE loyalty
(
	 traderId SMALLINT NOT NULL PRIMARY KEY
	,loyaltyLvl SMALLINT
	,reqLvl SMALLINT
	,reqRep SMALLINT
	,reqSales SMALLINT
	,FOREIGN KEY (currId) REFERENCES currency(currId)
);

CREATE TABLE trader
(
	 traderId SMALLINT NOT NULL PRIMARY KEY
	,traderName VARCHAR(20)
	,bio VARCHAR(100)
	,wares VARCHAR(50)
);

CREATE TABLE location
(
	 locationId SMALLINT NOT NULL PRIMARY KEY
	,name VARCHAR(30)
	,desc VARCHAR(100)
	,status VARCHAR(10)
);

CREATE TABLE quest
(
	 questId SMALLINT NOT NULL PRIMARY KEY
	,questName VARCHAR(10)
	,desc VARCHAR(100)
	,prevQuestId SMALLINT
	SMALLINT
	SMALLINT
	SMALLINT
	SMALLINT
);


-- ************************************** "public"."currency"

CREATE TABLE "public"."currency"
(
 "CurrId"   int NOT NULL,
 "currType" varchar(20) NOT NULL

);

CREATE UNIQUE INDEX "PK_currency" ON "public"."currency"
(
 "CurrId"
);

--drop table slot
CREATE TABLE slot
(
	"slotId"	smallint NOT NULL GENERATED ALWAYS AS IDENTITY,
	"slot"		varchar(50)
);

-- Insert values into slot table
INSERT INTO public.slot("slot")
VALUES('Primary'),('Secondary'),('Melee'),('Headwear'),('Earpiece'),('Face Cover'),('Body Armor'),
('Armband'),('Eyewear'),('Chest Rig'),('Backpack');

--SELECT * FROM slot

--drop table itemType
CREATE TABLE itemType
(
	"itemTypeId"	smallint NOT NULL GENERATED ALWAYS AS IDENTITY,
	"itemType"		varchar(50)
);
--truncate table itemType
INSERT INTO public.itemType("itemType")
VALUES('Assault rifle'),('Assault carbine'),('Light machine gun'),('Submachine gun'),('Shotgun'),('Designated marksman rifle'),
('Sniper rifle'),('Pistol'),('Melee weapon'),('Fragmentation grenade'),('Smoke grenade'),('Stun grenade'),('Mask'),('Armor vest'),('Helmet'),('Armored chest rig'),
('Chest rig'),('Night vision'),('Goggles'),('Backpack'),('Cap'),('Head Mount'),('Mask'),('Bandana'),('Hat'),('Bag'),('Headset')
--,(''),(''),(''),(''),(''),('');
--select * from itemType

--drop table public.weaponProperties
-- ************************************** "public"."weaponProperties"
/*
CREATE TABLE public.weaponProperties
(
 weaponId	      		smallint NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
 itemTypeId	 			smallint NOT NULL,
 slotId        			smallint NOT NULL,
 name					varchar(50),
 weight     	   		varchar(10),
 gridSize   	  		varchar(10),
 price      	 		varchar(5),
 traderId   	   		smallint,
 opRes    				smallint,
 rarity      	 		smallint,
 repair 		 		smallint,
 fireModes     			varchar(50),
 sightingRange      	smallint,
 ergo       			smallint,
 muzzleVelocity   	    varchar(10),
 effectiveDistance 	    varchar(6),
 accuracy      			smallint,
 recoilvert     		smallint,
 recoilHoriz     		smallint,
 rpm   					smallint,
 caliber       			varchar(30),
 defaultAmmo        	varchar(50),
 defaultmag				varchar(50)
);
*/ 
--truncate table weaponProperties
/* --Copy data from csv
COPY weaponProperties(itemTypeId,slotId,name,weight,gridSize,price,traderId,opRes,
					  rarity,repair,fireModes,sightingRange,ergo,muzzleVelocity,effectiveDistance,
					  accuracy,recoilVert,recoilHoriz,rpm,caliber,defaultAmmo,defaultMag)
FROM 'd:\test.csv' DELIMITER ',' CSV HEADER;
*/

SELECT * FROM weaponProperties

-- Fix an issue with the default ammo type on two shotguns
UPDATE weaponproperties
SET defaultammo = '12x70 Buckshot'
WHERE defaultammo LIKE '%560d5e524bdc2d25448b4571%'

-- Set column types to more appropriate values since the ones assigned by python are larger thgan needed
ALTER TABLE weaponproperties
ALTER COLUMN itemtypeid 		TYPE smallint,
ALTER COLUMN slotId 			TYPE smallint,
ALTER COLUMN name				TYPE varchar(100),
ALTER COLUMN weight   			TYPE varchar(10),
ALTER COLUMN gridSize 			TYPE varchar(10),
ALTER COLUMN price     			TYPE varchar(10),
ALTER COLUMN traderId   		TYPE varchar(200),
ALTER COLUMN opRes    			TYPE smallint USING (opRes::smallint),
ALTER COLUMN rarity   			TYPE varchar(10),
ALTER COLUMN repair 			TYPE smallint USING (repair::smallint),
ALTER COLUMN fireModes  		TYPE varchar(50),
ALTER COLUMN sightingRange 		TYPE smallint USING (sightingRange::smallint),
ALTER COLUMN ergo    			TYPE smallint USING (ergo::smallint),
ALTER COLUMN muzzleVelocity 	TYPE varchar(10),
ALTER COLUMN effectiveDistance 	TYPE varchar(6),
ALTER COLUMN accuracy    		TYPE smallint USING (accuracy::smallint),
ALTER COLUMN recoilVert   		TYPE smallint USING (recoilvert::smallint),
ALTER COLUMN recoilHoriz  		TYPE smallint USING (recoilHoriz::smallint),
ALTER COLUMN rpm   				TYPE smallint USING (rpm::smallint),
ALTER COLUMN caliber     		TYPE varchar(50),
ALTER COLUMN defaultAmmo    	TYPE varchar(50),
ALTER COLUMN defaultMag			TYPE varchar(50)

-- Need to hand jam grenade and melee weapons

-- DROP TABLE equipmentproperties
--Start Equipment
SELECT * FROM equipmentproperties
where slotid = 5
