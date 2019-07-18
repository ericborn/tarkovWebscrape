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
('Sniper rifle'),('Pistol'),('Melee weapon'),('Fragmentation grenade'),('Smoke grenade'),('Stun grenade'),('Mask'),('Armor vest'),
('Helmet'),('Armored chest rig'),('Chest rig'),('Night vision'),('Goggles'),('Backpack'),('Cap'),('Head Mount'),('Mask'),
('Bandana'),('Hat'),('Bag'),('Headset'),('Stimulator'),('Drug'),('Medical item'), ('Consumable'),('medikit')
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

-- DROP TABLE medical
CREATE TABLE medical
(
	medId	   SMALLINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	itemtypeid SMALLINT,
	slotid SMALLINT,
	name VARCHAR(100),
	weight varchar(10),
	gridsize VARCHAR(7),
	price VARCHAR(10),
	traderid SMALLINT,
	rarity VARCHAR(30),
	hpUse SMALLINT,
	hpTotal SMALLINT,
	removes VARCHAR(500),
	adds VARCHAR(500),
	buff VARCHAR(500),
	debuff VARCHAR(500),
	uses SMALLINT,
	usetime VARCHAR(4),
	spawnchance VARCHAR(4),
	lootxp SMALLINT,
	examxp SMALLINT
	--FOREIGN KEY (currId) REFERENCES currency(currId)
);
--select * from itemType
--select * from medical

--truncate table medical

--!!!!! Check item types!!!!!!!!!
INSERT INTO public.medical(itemtypeid, slotid, name, weight, gridsize, price, traderid, rarity, hpUse, hpTotal, 
						   removes, adds, Buff, Debuff, uses, usetime, spawnchance, lootxp, examxp)
VALUES (27, NULL, 'Augmentin antibiotic pills', '0.1 kg', '1x1', '₽3,800', NULL, NULL, NULL, NULL, 'Pain', 
		'On Painkillers for 230s', NULL, NULL, 4, '3s', '5%', 20, 8),
	   
	   (27, NULL, 'Analgin painkillers', '0.3 kg', '1x1', '₽8,900', NULL, NULL, NULL, NULL, 'Pain, Toxication', 
		'On Painkillers for 260s', NULL, NULL, 1, '5s', '5%', 50, 25),
	   
	   (27, NULL, 'Morphine injector', '0.1 kg', '1x1', '₽5,500', NULL, 'Rare', NULL, NULL, 'Pain, Contusion', 
		'On Painkillers for 400s', NULL, NULL, 1, '2s', '7%', 20, 8),
	   
	   (27, NULL, 'Ibuprofen painkiller', '0.1 kg', '1x1', '₽7,500', NULL, 'Rare', NULL, NULL, 'Pain, Contusion', 
		'On Painkillers for 600s', NULL, NULL, 12, '5s', NULL, NULL, NULL),
	   
	   (27, NULL, 'Aseptic Bandage', '0.04 kg', '1x1', '₽1,300', NULL, 'Common', NULL, NULL, 'Bloodloss', 'Fresh wound', 
	    NULL, NULL, 1, '4s', '15%', 10, 10),
	   
	   (27, NULL, 'Army Bandage', '0.043 kg', '1x1', '₽1,830', NULL, 'Rare', NULL, NULL, 'Bloodloss', 'Fresh wound', 
	   	NULL, NULL, 2, '4s', '20%', 20, 2),
	   
	   (29, NULL, 'Condensed milk', '0.4 kg', '1x1', '₽8,500', NULL, NULL, NULL, NULL, 'Bloodloss, Hydration -50', 
		'Energy +60, Fresh wound', NULL, NULL, 1, '4s', NULL, 50, 20),
	   
	   (30, NULL, 'AI-2', '0.5 kg', '1x1', '₽3,250', NULL, 'Common', 50, 100, 'Radiation Exposure', 'Fresh wound', 
	   	NULL, NULL, NULL, '2s', '15%', 25, 10),
	   
	   (27, NULL, 'Car first aid kit', '1 kg', '2x1', '₽4,450', NULL, 'Common', 70, 220, 'Bloodloss, Toxication, Radiation Exposure', 
		'Fresh wound', NULL, NULL, NULL, '3s', '10%', 25, 10),
	   
	   (27, NULL, 'Salewa first aid kit', '0.6 kg', '2x1', '₽7,500', NULL, 'Rare', 85, 400, 'Bloodloss', 'Fresh wound', 
	   NULL, NULL, NULL, '3s', '9%', 20, 6),
	   
	   (27, NULL, 'IFAK personal tactical first aid kit', '0.8 kg', '1x1', '₽10,850', NULL, 'Super rare', 50, 300, 
		'Bloodloss, Toxication, Radiation Exposure', 'Fresh wound', NULL, NULL, NULL, '3s', '7%', 25, 10),
	   
	   
	   (27, NULL, 'Grizzly first aid kit', '1.6 kg', '2x2', '₽17,000', NULL, 'Super rare', 175, 1800, 
	    'Bloodloss, fracture, contusion, pain', 'Fresh wound', NULL, NULL, NULL, '5s', '1%', 40, 10),
	   
	   
	   (27, NULL, 'Immobilizing splint', '0.17 kg', '1x1', '₽1,855', NULL, 'Common', NULL, NULL, 'Fracture', NULL, 
	   NULL, NULL, 1, '5s', '15%', 40, 2),
	   
	   
	   (27, NULL, 'Alu Immobilizing splint', '0.22 kg', '1x1', '₽5,980', NULL, NULL, NULL, NULL, 'Fracture', NULL, 
	   NULL, NULL, 5, '3s', NULL, NULL, NULL),
	   
	   (27, NULL, 'Vaseline', '0.01 kg', '1x1', '₽8,060', NULL, NULL, NULL, NULL, 'Pain', 'On Painkillers for 500s', 
	   NULL, NULL, 10, '6s', NULL, 100, 4),
	   
	   (27, NULL, 'Golden star balm', '0.1 kg', '1x1', '₽18,510', NULL, 'Super rare',  NULL, NULL,
		'Contusion, Pain, Toxication, Radiation Exposure for 600s', 'On Painkillers for 600s', 
		'Energy and Hydration recovery, 1 per/s for 5s', NULL, 10, '7s', '1%', 250, 4),
	   
	   (27, NULL, 'Combat stimulant SJ1', '0.5 kg', '1x1', '₽27,610', NULL, NULL, NULL, NULL, NULL, NULL,
	    'Endurance for 180 seconds (+25), Strength for 180 seconds (+25), Stress Resistance for 180 seconds (+25)', 
		'Energy recovery for 200 seconds (-0.25), hydration recovery for 200 seconds (-0.3)', 1, '2s', '1%', 20, 8),

	   (27, NULL, 'Regenerative stimulant injector', '0.1 kg', '1x1', '₽29,100', NULL, 'Rare', NULL, NULL, 'Contusion', NULL, 
	    'Metabolism, Immunity by +20 for 90s, Health regeneration by 30 for 30s, energy recovery by 1 for 30s', 
		'Energy recovery by -4 for 20s, Health and Endurance by -10 for 60s', 1, '2s', '2%', 20, 8),
	   
	   (27, NULL, 'Combat stimulant injector SJ6', '0.1 kg', '1x1', '₽21,500', NULL, 'Rare', NULL, NULL, NULL, NULL, 
	    'Max stamina for 240 seconds (+50), Stamina recovery rate for 240 seconds (+2.5)', 
		'Hands tremor for 60 seconds, tunnel effect for 30 seconds', 1, '2s', '5%', 20, 8),
	   
	   (27, NULL, 'Propital', '0.1 kg', '1x1', '₽16,200', NULL, 'Super rare', NULL, NULL, 'Pain, Contusion, Toxication', NULL,
		'Metabolism for 300 seconds (+20), Health for 300 seconds (+20), Vitality for 300 seconds (+20), 
		health regeneration for 300 seconds (+1)', 
		'hand tremor for 300 seconds, tunnel effect for 60 seconds, pain for 120 seconds', 1, '2s', '7%', 20, 8),
	   
	   (27, NULL, 'Hemostatic drug Zagustin', '0.1 kg', '1x1', '₽25,800', NULL, 'Rare', NULL, NULL, 'Bloodloss', NULL, 
	    'Vitality for 180 seconds (+20), Prevents bleeding for 180 seconds', 
		'hydration recovery for 50 seconds (-1.4), Causes hand tremor for 120 seconds, Decreases Metabolism for 180 seconds (-10)', 
		1, '2s', '2%', 20, 8),
	   
	   (27, NULL, 'Adrenaline injector', '0.1 kg', '1x1', '₽24,200', NULL, NULL, NULL, NULL, 'Pain, Contusion', 'On Painkillers for 600s', 
	    'Endurance for 60 seconds (+20), Strength for 60 seconds (+20), Mag Drills for 60 seconds (+20), 
		health regeneration for 15 seconds (+4)', 
	    'Energy recovery for 30 seconds (-0.8), hydration recovery for 30 seconds (-1), Stress Resistance for 60 seconds (-10)', 
		1, '2s', '4%', 20, 8)

