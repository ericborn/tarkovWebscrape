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

-- ************************************** "public"."armorProperties"

CREATE TABLE "public"."armorProperties"
(
 "armorId"       integer NOT NULL,
 "slotId"        integer NULL,
 "itemTypeId"    int NULL,
 "weight"        int NOT NULL,
 "traderId"      integer NOT NULL,
 "gridSize"      varchar(50) NOT NULL,
 "material"      varchar(50) NOT NULL,
 "armorClass"    smallint NOT NULL,
 "zone"          varchar(50) NOT NULL,
 "armorSegments" varchar(50) NOT NULL,
 "durability"    smallint NOT NULL,
 "ricochet"      varchar(50) NOT NULL,
 "penMove"       varchar(50) NOT NULL,
 "penTurn"       varchar(50) NOT NULL,
 "penErgo"       varchar(50) NOT NULL,
 "penSound"      varchar(50) NOT NULL,
 "blocksEar"     varchar(3) NOT NULL,
 "blocksEye"     varchar(3) NOT NULL,
 "blocksFace"    varchar(3) NOT NULL,
 "lootXp"        smallint NOT NULL,
 "examXP"        smallint NOT NULL,
 CONSTRAINT "FK_290" FOREIGN KEY ( "slotId" ) REFERENCES "slot" ( "slotId" ),
 CONSTRAINT "FK_294" FOREIGN KEY ( "itemTypeId" ) REFERENCES "public"."itemType" ( "itemTypeId" ),
 CONSTRAINT "FK_305" FOREIGN KEY ( "traderId" ) REFERENCES "public"."trader" ( "traderId" )
);

CREATE UNIQUE INDEX "PK_properties" ON "public"."armorProperties"
(
 "armorId"
);

CREATE INDEX "fkIdx_290" ON "public"."armorProperties"
(
 "slotId"
);

CREATE INDEX "fkIdx_294" ON "public"."armorProperties"
(
 "itemTypeId"
);

CREATE INDEX "fkIdx_305" ON "public"."armorProperties"
(
 "traderId"
);

--drop table public.weaponProperties
-- ************************************** "public"."weaponProperties"
CREATE TABLE public.weaponProperties
(
 "weaponId"      		smallint NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
 "itemTypeId"	 		smallint NOT NULL,
 "slotId"        		smallint NOT NULL,
 "name"					varchar(50),
 "weight"        		varchar(10),
 "gridSize"      		varchar(10),
 "price"      	 		varchar(5),
 "traderId"      		smallint,
 "opRes"    			varchar(1),
 "rarity"       		varchar(1),
 "repair" 		 		varchar(10),
 "fireModes"     		varchar(50),
 "sightingRange"      	smallint,
 "ergo"       			smallint,
 "muzzleVelocity"       varchar(10),
 "effectiveDistance"    varchar(6),
 "accuracy"      		varchar(1),
 "recoilvert"     		smallint,
 "recoilHoriz"     		smallint,
 "rpm"    				smallint,
 "caliber"        		varchar(30),
 "defaultAmmo"        	varchar(50),
 "defaultmag"			varchar(50)
);

--drop table slot
CREATE TABLE slot
(
	"slotId"	smallint NOT NULL GENERATED ALWAYS AS IDENTITY,
	"slot"		varchar(50)
);

-- Insert values into slot table
INSERT INTO public.slot("slot")
VALUES('Primary'),('Secondary'),('Melee'),('Headwear'),('Earpiece'),('Face Cover'),('Body Armor'),('Armband'),('Eyewear'),('Chest Rig'),('Backpack');

--SELECT * FROM slot

--drop table itemType
CREATE TABLE itemType
(
	"itemTypeId"	smallint NOT NULL GENERATED ALWAYS AS IDENTITY,
	"itemType"		varchar(50)
);

INSERT INTO public.itemType("itemType")
VALUES('Assault rifle'),('Assault carbine'),('Light machine gun'),('Submachine gun'),('Shotgun'),('Designated marksman rifle'),
('Sniper rifle'),('Pistol'),('Melee weapon'),('Fragmentation grenade'),('Smoke grenade'),('Stun grenade'),('Mask'),('Armor vest'),('Helmet'),('Armored chest rig'),
('Chest rig'),('Night vision'),('Goggles'),('Backpack');
--,(''),(''),(''),(''),(''),(''),(''),(''),(''),(''),(''),('');

SELECT * FROM itemType