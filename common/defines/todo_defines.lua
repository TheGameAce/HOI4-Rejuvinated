-- TODO: Manually go over those defines

NDefines.NMilitary.NEW_OPERATIVE_RANDOM_PERSONALITY_TRAIT_CHANCES = {  			-- chances to gain a personality trait for new operatives
		0.6, -- up from vanilla 50% for first trait
		0.2  -- up from vanilla 10% for second trait after that
	}
	
NDefines.NMilitary.NEW_OPERATIVE_RANDOM_BASIC_TRAIT_CHANCES = {  				-- chances to gain a basic trait for new operatives
		0.35, -- up from vanilla 25% for first trait
		0.15  -- up from vanilla 5% for second trait after that
	}
	
NDefines.NOperatives.AGENCY_UPGRADE_PER_OPERATIVE_SLOT = 4							-- (normaly 5) Number of upgrade needed to unlock an additional operative slot
NDefines.NOperatives.MAX_OPERATIVE_SLOT_FROM_AGENCY_UPGRADES = 8					-- (normaly 1) max operative slots gained from upgrades
NDefines.NOperatives.INTEL_NETWORK_GAIN_RATE_ON_WRONG_CONTROLLER = -9.9				-- (normaly -10.0) Amount of network strength lost in a state when it does not have the right controller anymore
NDefines.NOperatives.INTEL_NETWORK_GAIN_RATE_ON_OUT_OF_RANGE = -1.57				-- (normaly -1.75) Amount of network strength lost in a state that has the right controller but is out of range of any operative
			--may come back to below, but makes much more of a diffrence than i thaught
		--NDefines.NOperatives.INTEL_NETWORK_MIN_VP_TO_TARGET = 10,					-- (normaly 15) The minimum value of the highest VP in a state to consider the state as a valid target to start building an intel network
NDefines.NOperatives.INTEL_NETWORK_OPERATIVE_GAIN_STACKING_FACTOR = 0.6				-- (normaly 0.5) When multiple operative are present in the same location, this factor is applied for each operative with a lower gain than the max. So if operatives have the gain [ 3, 1, 2 ] in the same location, it is sorted to [ 1, 2, 3 ] then converted to [ 1*D^2, 2*D^1, 3 ], with D being this define, so if D=0.5 we have [ 0.25, 1, 3 ] and the final gain from operative at this location will be 4.25. Putting this define to 0 is equivalent to considering the maximum value only.

NDefines.NOperatives.QUIET_INTEL_NETWORK_DAILY_XP_GAIN = 0.112						-- (normaly 0.0)

	-- used for calculating how many operatives will a spy master gain from its faction members
	-- first number in every now is number of operatives gained
	-- second number is total factory needed (mil and civ) for giving previous ratio
	-- NORMAL BELOW
	--0.0, 		0.0, 	-- 0 operative for [0, 10)
	--0.25,  	10.0,	-- 0.25 operative for [10, 50)
	--0.5, 		50.0,	-- 0.5 operative for >= 50

NDefines.NOperatives.OPERATIVE_SLOTS_FROM_FACTION_MEMBERS_FOR_SPY_MASTER = {
		0.0, 	0.0, -- 0 operative for [0, 5)
		0.1,  	5.0, -- 0.1 operative for [5, 10)
		0.25, 	10.0, -- 0.25 operative for [10, 25)
		0.5,  	25.0, -- 0.5 operative for [25, 50)
		0.75,  	50.0, -- 0.75 operative for [50, 75)
		1.0,  	75.0, -- 1 operative for [75, 100)
		1.5,  	100.0, -- 1.5 operative for >= 100
	}
	
NDefines.NOperatives.OPERATIVE_BASE_INTEL_NETWORK_GAIN = 0.32				-- (normaly 0.4) Base amount of network strength gain per day provided by an operative
NDefines.NOperatives.COUNTER_INTELLIGENCE_STACKING_FACTOR = 0.6								-- (normaly 0.5) Multiplier applied to each operative after the first one. So if we have the following counter intelligence rating values [ 0.1, 0.3, 0.2 ], the factor is applied twice for the lowest value and once for the 2nd lowest one as such : [ 0.3, 0.2 * D, 0.1 * D * D ] and then the result is summed up to give the final rating value
			--no change made, but kept in case i change my mind
		--NDefines.NOperatives.COUNTER_INTELLIGENCE_DAILY_XP_GAIN = 0.112,

NDefines.NOperatives.BOOST_IDEOLOGY_MAX_DRIFT_BY_OPERATIVE = 0.2			-- (normaly 0.25) the maximum drift an operative can cause, a negative value means no maximum
NDefines.NOperatives.BOOST_IDEOLOGY_DRIFT_STACKING_FACTOR = 0.6				-- (Normaly 0.5) multiplied to the drift of an operative for each operative after the first one, with the greatest drift. So if we have the following drift values [ 0.1, 0.3, 0.2 ], the factor is applied twice for the lowest value and once for the 2nd lowest one as such : [ 0.3, 0.2 * D, 0.1 * D * D ] and then the result is summed up to give the final drift value.
NDefines.NOperatives.BOOST_IDEOLOGY_DAILY_XP_GAIN = 0.3						-- (normaly 0.274)
NDefines.NOperatives.OPERATIVE_BASE_BOOST_IDEOLOGY = 0.08					-- (normaly 0.1) Base amount of daily ideology drift provoked by an operative
NDefines.NOperatives.OPERATIVE_BASE_PROPAGANDA_POWER = 0.0004				-- (normaly 0.0005) Base amount of daily war support and stability change when an operative is assigned to propaganda
NDefines.NOperatives.PROPAGANDA_OPERATIVE_STACKING_FACTOR = 0.6				-- (normaly 0.5) Multiplied to the Stability/WarSupport drift values of each operative after the one with the greatest values. The process is done separatly for Stability and WarSupport
			--no change made, but kept in case i change my mind
		--NDefines.NOperatives.PROPAGANDA_COUNTRY_STACKING_FACTOR = 0.5,			-- Multiplied to the Stability/WarSupport drift values of each country after the one with the greatest values. The process is done separatly for Stability and WarSupport
NDefines.NOperatives.PROPAGANDA_DAILY_XP_GAIN = 0.420						-- (normaly 0.35
			--no change made, but kept in case i change my mind
		--NDefines.NOperatives.OPERATIVE_BASE_ROOT_OUT_RESISTANCE_EFFICIENCY = 1.0,	-- The base efficiency of an operative at the RootOutResistance mission (this is a percentage, 1.0 == 100%)
NDefines.NOperatives.OPERATIVE_BASE_ROOT_OUT_RESISTANCE_EFFICIENCY = 0.9	-- (normaly 1.0) The base efficiency of an operative at the RootOutResistance mission (this is a percentage, 1.0 == 100%)
NDefines.NOperatives.ROOT_OUT_RESISTANCE_STACKING_FACTOR = 0.6				-- (normaly 0.5) Multiplied to each operative efficiency after the first one
NDefines.NOperatives.ROOT_OUT_RESISTANCE_RANGE_STEP_FACTOR = 0.6			-- (normaly 0.5) Multiplied to the summed up efficiency from all operative operating in a same state to determine the efficiency in neighboring states
NDefines.NOperatives.ROOT_OUT_RESISTANCE_DAILY_XP_GAIN = 0.08				-- (normaly 0.068)
NDefines.NOperatives.OPERATIVE_BASE_CONTROL_TRADE_DRIFT = 0.4				-- (normaly 0.5) The base daily drift in trade influence caused by an operative
NDefines.NOperatives.CONTROL_TRADE_STACKING_FACTOR = 0.6					-- (normaly 0.6) Multiplied to the drift of each operative after the first one
NDefines.NOperatives.CONTROL_TRADE_DAILY_XP_GAIN = 0.164					-- (normaly 0.137)

NDefines.NOperatives.DIPLOMATIC_PRESSURE_OPERATIVE_STACKING_FACTOR = 0.6	-- (normaly 0.5) The diminishing return factor to apply to operative working for the same faction after the first one. Operatives operating for a same faction are ranked by their efficiency and their opinion and tension drift are individually applyied a stacking factor like so: DRIFT * STACKING_FACTOR^RANK where RANK is a value from 0 to the number of operative -1 where the opperative with the highest drift value has rank 0
NDefines.NOperatives.DIPLOMATIC_PRESSURE_DAILY_XP_GAIN = 0.164				-- (Normaly 0.137)
NDefines.NOperatives.MAX_RECRUITED_OPERATIVES = 16							-- (Normaly 10)
	
NDefines.NOperatives.OPERATION_COMPLETION_XP = 24							-- (normaly 18)

NDefines.NOperatives.ON_CAPTURE_COUNTERINTELLIGENCE_OPERATIVE_XP_GAIN = 120	-- (normaly 100) Xp gain when an enemy operative is captured in the country the operative is assigned to counter intelligence to. Apply to a single randomly selected operative

    
NDefines.NIntel.RADAR_INTEL_STACKING_FACTOR = 0.6							-- (Normaly 0.5) Used when multiple radars cover the same province

NDefines.NIntel.RECON_PLANE_INTEL_BASE = 0.024								-- (normaly 0.02) intel base amount for a strategic area per plane

