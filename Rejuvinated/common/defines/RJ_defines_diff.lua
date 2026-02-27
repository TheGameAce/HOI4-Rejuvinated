-- NGame
NDefines.NGame.END_DATE = "1959.1.1.1"

-- NCountry
NDefines.NCountry.LOCAL_MANPOWER_ACCESSIBLE_NON_CORE_FACTOR = 0.03 -- accessible recruitable factor base
NDefines.NCountry.STARTING_COMMAND_POWER = 10.0 -- starting command power for every country
NDefines.NCountry.BASE_MAX_COMMAND_POWER = 300.0 -- base value for maximum command power

-- NProduction
NDefines.NProduction.DEFAULT_MAX_NAV_FACTORIES_PER_LINE = 15
NDefines.NProduction.FLOATING_HARBOR_MAX_NAV_FACTORIES_PER_LINE = 15
NDefines.NProduction.CAPITAL_SHIP_MAX_NAV_FACTORIES_PER_LINE = 15
NDefines.NProduction.RAILWAY_GUN_MAX_MIL_FACTORIES_PER_LINE = 10
NDefines.NProduction.RESOURCE_TO_ENERGY_COEFFICIENT = 12.0 -- How much energy per coal produces
NDefines.NProduction.BASE_COUNTRY_ENERGY_PRODUCTION = 12.0 -- The base energy production of a country
NDefines.NProduction.BASE_ENERGY_COST = 0.15 -- How much energy per factory consumes
NDefines.NProduction.ENERGY_COST_CAP = 4 -- Maximum energy cost per factory
NDefines.NProduction.ENERGY_SCALE_PER_TRADE_FACTORY_EXPORT = 0.10 -- Factor of how many of the factories gained from trade is affects the energy cost scaling
NDefines.NProduction.EQUIPMENT_BASE_LEND_LEASE_WEIGHT = 0.5 -- Base equipment lend lease weight
NDefines.NProduction.EQUIPMENT_MODULE_ADD_XP_COST = 3.0 -- XP cost for adding a new equipment module in an empty slot when creating an equipment variant.
NDefines.NProduction.EQUIPMENT_MODULE_REPLACE_XP_COST = 4.0 -- XP cost for replacing one equipment module with an unrelated module when creating an equipment variant.
NDefines.NProduction.EQUIPMENT_MODULE_CONVERT_XP_COST = 2.0 -- XP cost for converting one equipment module to a related module when creating an equipment variant.
NDefines.NProduction.MINIMUM_NUMBER_OF_FACTORIES_TAKEN_BY_CONSUMER_GOODS_PERCENT = 0.05 -- The minimum number of factories we have to put on consumer goods, in percent.

-- NPolitics
NDefines.NPolitics.ARMY_LEADER_MAX_COST = 50 -- max cost BEFORE modifiers
NDefines.NPolitics.NAVY_LEADER_MAX_COST = 50 -- max cost BEFORE modifiers

-- NMilitary
NDefines.NMilitary.MAX_ARMY_EXPERIENCE = 1000 --Max army experience a country can store
NDefines.NMilitary.MAX_NAVY_EXPERIENCE = 1000 --Max navy experience a country can store
NDefines.NMilitary.MAX_AIR_EXPERIENCE = 1000 --Max air experience a country can store
NDefines.NMilitary.LAND_AIR_COMBAT_STR_DAMAGE_MODIFIER = 0.05 -- air global strength damage modifier
NDefines.NMilitary.LAND_AIR_COMBAT_ORG_DAMAGE_MODIFIER = 0.10 -- air global organization damage modifier
NDefines.NMilitary.ENEMY_AIR_SUPERIORITY_DEFENSE = 0.70 -- more AA attack will approach this amount of help (diminishing returns)
NDefines.NMilitary.ENEMY_AIR_SUPERIORITY_DEFENSE_STEEPNESS = 112 -- how quickly defense approaches the max impact diminishing returns curve
NDefines.NMilitary.UNIT_LEADER_USE_NONLINEAR_XP_GAIN = false -- Whether unit leader XP gain is scaled by 1/<nr_of_traits>

-- NAir
NDefines.NAir.ANTI_AIR_ATTACK_TO_DAMAGE_REDUCTION_FACTOR = 1.0 -- Balancing value to convert equipment stat anti_air_attack to the damage reduction modifier apply to incoming air attacks against units with AA.

-- NNavy
NDefines.NNavy.NAVAL_HOMEBASE_CALCULATION_DISTANCE_CUTOFF = 1000 -- Tuning parameter for homebase calculation. Distance to normalize against. Everything above said value will be treated as score = 0.
NDefines.NNavy.NAVAL_HOMEBASE_BUILDING_SCORE_FACTOR = 0.02 -- Tuning parameter for homebase calculation. Multiplier for how much the level of the naval base impacts its total score.
NDefines.NNavy.COMBAT_MIN_HIT_CHANCE = 0.05 -- never less hit chance then this?
NDefines.NNavy.COMBAT_RETREAT_DECISION_CHANCE = 0.22 -- There is also random factor in deciding if we should retreat or not. That causes a delay in taking decision, that sooner or later will be picked. It's needed so damaged fast ships won't troll the combat.
NDefines.NNavy.REPAIR_AND_RETURN_PRIO_LOW = 0.2 -- % of total Strength. When below, navy will go to home base to repair.
NDefines.NNavy.REPAIR_AND_RETURN_PRIO_MEDIUM = 0.5 -- % of total Strength. When below, navy will go to home base to repair.
NDefines.NNavy.REPAIR_AND_RETURN_PRIO_HIGH = 0.9 -- % of total Strength. When below, navy will go to home base to repair.
NDefines.NNavy.REPAIR_AND_RETURN_PRIO_LOW_COMBAT = 0.6 -- % of total Strength. When below, navy will go to home base to repair (in combat).
NDefines.NNavy.REPAIR_AND_RETURN_PRIO_MEDIUM_COMBAT = 0.3 -- % of total Strength. When below, navy will go to home base to repair (in combat).
NDefines.NNavy.REPAIR_AND_RETURN_PRIO_HIGH_COMBAT = 0.1 -- % of total Strength. When below, navy will go to home base to repair (in combat).
NDefines.NNavy.REPAIR_AND_RETURN_AMOUNT_SHIPS_MEDIUM = 0.4 -- % of total damaged ships, that will be sent for repair-and-return in one call.
NDefines.NNavy.REPAIR_AND_RETURN_AMOUNT_SHIPS_HIGH = 0.8 -- % of total damaged ships, that will be sent for repair-and-return in one call.
NDefines.NNavy.NAVAL_TRANSFER_BASE_SPEED = 14 -- base speed of units on water being transported
NDefines.NNavy.AGGRESION_MULTIPLIER_FOR_COMBAT = 1.2 -- ships are more aggresive in combat
NDefines.NNavy.AGGRESSION_TORPEDO_EFFICIENCY_ON_LIGHT_SHIPS = 0.1 -- ratio for scoring for different gun types against light ships
NDefines.NNavy.AGGRESSION_TORPEDO_EFFICIENCY_ON_HEAVY_SHIPS = 1.1 -- ratio for scoring for different gun types against heavy ships
NDefines.NNavy.MIN_SHIP_COUNT_FOR_TASK_FORCE_ROLE_ASSIGNMENT = 4 -- define the minimum number of ship that should be in a task force for it to be considered a patrol or an escort task force (used to the insignia assignment, see TASK_FORCE_ROLE_TO_INSIGNIA)

-- NAI
NDefines.NAI.DAYS_BETWEEN_CHECK_BEST_DOCTRINE = 7 -- Recalculate desired best doctrine to unlock with this many days inbetween.
NDefines.NAI.UPGRADE_PERCENTAGE_OF_FORCES = 0.03 -- How big part of the army that should be considered for upgrading
NDefines.NAI.MANPOWER_RATIO_REQUIRED_TO_PRIO_MOBILIZATION_LAW = 0.4 -- percentage of manpower in field is desired to be buffered for AI when it has upcoming wars or already at war. if it has less manpower, it will prio manpower laws
NDefines.NAI.UPGRADES_DEFICIT_LIMIT_DAYS = 7 -- Ai will avoid upgrading units in the field to new templates if it takes longer than this to fullfill their equipment need
NDefines.NAI.AIFC_PATH_COST_TRN_MOUNTAINS = 2.0
NDefines.NAI.AIFC_PATH_COST_TRN_FOREST = 1.5
NDefines.NAI.AIFC_PATH_COST_TRN_DESERT = 1.5
NDefines.NAI.CONVOY_RAIDING_TARGET_RECALC_DAYS = 3 -- Each X days, the AI will reevaluate which regions to convoy raid (because enemy convoy usage or trade routes might change)
NDefines.NAI.AI_OBJECTIVE_DEFAULT_TARGET_RECALC_DAYS = 0 -- Each X days, the AI will reevaluate which regions to target for naval missions (this is the default value, but can be overriden by specific objectives, see CONVOY_RAIDING_TARGET_RECALC_DAYS)

-- NSupply
NDefines.NSupply.CAPITAL_SUPPLY_BASE = 7.0 -- base supply for capital
NDefines.NSupply.INFRA_TO_SUPPLY = 0.8 -- each level of infra gives this many supply

-- NProject
NDefines.NProject.SCIENTIST_BASIC_RESEARCH_DAILY_XP_GAIN = 0.33 -- Daily experience gain for doing basic research
NDefines.NProject.BASIC_RESEARCH_TECHNOLOGY_BONUS_DIMINISHING_RETURN_FACTOR = 0.1 -- Diminishing return on BASIC_RESEARCH_TECHNOLOGY_BONUS_FACTOR for each extra scientist performing basic research for multiple facilities.

-- NDoctrines
NDefines.NDoctrines.MAX_MONTHLY_MASTERY_GAIN = 50.0 -- Monthly mastery gain will not exceed this value
NDefines.NDoctrines.MASTERY_BAR_ANIMATION_SPEED_PER_DAILY_MASTERY = 5.0 -- Multiplier of how fast the mastery bar animates based on daily mastery gain
NDefines.NDoctrines.MASTERY_BAR_MAX_ANIMATION_SPEED = 50.0 -- Max speed of the mastery bar animation