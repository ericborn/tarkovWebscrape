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

-- ************************************** "public"."weaponProperties"
CREATE TABLE "public"."weaponProperties"
(
 "weaponId"      		smallint NOT NULL GENERATED ALWAYS AS IDENTITY,
 "itemTypeId"	 		smallint NOT NULL,
 "slotId"        		smallint NOT NULL,
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
 "recoilHoriz"     		smallint,
 "recoilvert"     		smallint,
 "rpm"    				smallint,
 "caliber"        		varchar(10),
 "defaultAmmo"        	varchar(10),
 "defaultmag"			varchar(10)
);