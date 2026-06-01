import os
import re

HARDCODED_SKILLS = [
    "StunAttacks", "Stunning", "Multithrow", "WeaponThrow", "Health1", "ThrowableDamage", "Finisher",
    "combatprof1", "WeaponProficiency", "ChargeAttack", "GroundPound", "DeathFromAbove", "GroundPound2",
    "Health2", "Overpowered2b", "SpinAttack", "Stomp", "SpinAttack2", "KillFrenzy", "combatprof2",
    "Health3", "SilentKill", "UltimateFighter", "Dodge", "NageWaza", "NageWaza2", "Slide", "DropKick",
    "JumpOverZombie", "HealthRegen1", "LegBreaker", "DropKick2", "JumpOverZombie2", "runningprof1",
    "FastBreak", "SafeLanding", "Lookback", "FastBreak2", "SafeLanding2", "Tackle", "Tackle2",
    "FastBreak3", "runningprof2", "WallRun", "HealthRegen2", "UltimateRunner", "Survival101",
    "BackpackUpgrade2", "BlueprintsKnives", "Potions", "ShopDiscount1", "BoostsExtender",
    "BackpackUpgrade3", "BlueprintsGrenades", "ShopDiscount2", "BlueprintsFirecrackers",
    "ShopDiscount3", "craftingexpertise", "StatusTraps1", "StatusTraps2", "RepairLuck",
    "NimbleHands", "StatusCamouflage", "StatusCamouflage2", "StatusShield", "StatusShieldCrafting",
    "StatusHook", "ElementalCrit", "CraftingMaster", "UltimateSurvivor", "AutoSkill_ReputationLevel2",
    "AutoSkill_ReputationLevel3", "AutoSkill_ReputationLevel4", "AutoSkillReputationLevel5",
    "CarParts1", "CarNitro1", "CarNitro2", "CarAlarm", "CarRemoteControl", "CarCage1", "CarCage2",
    "CarCage3", "CarParts2", "CarMineLauncher", "CarParts3", "CarRammingBar1", "CarRammingBar2",
    "CarUVLights1", "CarUVLights2", "CarFuelTank1", "CarFuelTank2", "CarSuspension", "CarRepair1",
    "CarParts4", "CarElectricCage", "CarFlamethrower", "CarParts5", "AutoSkill_LegendLevel25",
    "AutoSkill_LegendLevel50", "AutoSkill_LegendLevel75", "AutoSkill_LegendLevel100",
    "AutoSkill_LegendLevel125", "AutoSkill_LegendLevel150", "AutoSkill_LegendLevel175",
    "AutoSkill_LegendLevel200", "AutoSkill_LegendLevel225", "AutoSkill_LegendLevel250",
    "LegendSkill_UnarmedDamage", "LegendSkill_OneHandedDamage", "LegendSkill_TwoHandedDamage",
    "LegendSkill_FirearmsDamage", "LegendSkill_BowDamage", "LegendSkill_ThrowingDamage",
    "LegendSkill_MaxStamina", "LegendSkill_MaxHealth", "LegendSkill_HealthRegeneration",
    "LegendSkill_HealingEfficiency", "ControlTheHordeSpitEnable", "ControlTheHordeSpitAmmo",
    "ControlTheHordeSpitDuration", "LightDisableEnable", "LightDisableAmmo", "LightDisableDuration",
    "DefensiveSmokeEnabled", "DefensiveSmokeAmmo", "DefensiveSmokeDuration", "ZombieGroundPoundMovement",
    "ZombieGroundPoundAirEnabled", "ZombieGroundPoundKnockback", "ZombieChargeAttack",
    "ZombieChargeAttackKnockback", "ZombieLeapfrog", "ZombiePounceSlam", "ZombieSprintUpgrade",
    "ZombieRopeLocoUpgrade", "SpitChargingEnabled", "SpitGroundPoundEnabled", "CamoSpitEnable",
    "ToxicSpitEnable", "UVHealEnable", "SkillStricterStaminaAuto", "SkillNightmareAuto", "Momentum", "RopeThrow"
]

HARDCODED_BUFFS = [
    "MedKitStrong", "MedKitPremium", "FoodSmall", "FoodNormal", "FoodLarge",
    "InfiniteFitnesAndSpeedIncrease", "NightVisionAndNightDamageBoost",
    "DamageResistatenMeleeAndBullet", "InfiniteStamina", "Ghul", "Christmas1_Resistance",
    "Christmas3_NightVision", "Christmas5_Stamina", "Christmas8_Speed", "Halloween1",
    "Halloween2", "Halloween3", "Halloween4", "Halloween5", "Halloween6", "Halloween7",
    "Eggnog", "GREBoost", "Mixture_WQ_Invert", "Mixture_WQ_SloMo", "Mixture_WQ_Rot",
    "Cloak", "InfiniteStaminaLvl1Hard", "Hellraid_Armor", "Hellraid_Speed",
    "Hellraid_B_Damage_DB_Stamina", "Hellraid_B_Speed_DB_Damage", "Hellraid_B_HealthRegen_DB_Stamina"
]

HARDCODED_CRAFTPLANS = [
    "Craft_Upgrade_Dam", "Craft_Upgrade_Dur", "Craft_Upgrade_Bal", "Craft_Upgrade_DamDur",
    "Craft_Upgrade_DamBal", "Craft_Upgrade_DurBal", "Craft_Upgrade_DamDurBal", "Craft_Upgrade_DamL2",
    "Craft_Upgrade_DurL2", "Craft_Upgrade_BalL2", "Craft_Upgrade_DamL2DurL2", "Craft_Upgrade_DamL2BalL2",
    "Craft_Upgrade_DurL2BalL2", "Craft_Upgrade_DamL2DurL2BalL2", "Craft_Upgrade_DamL2Dur",
    "Craft_Upgrade_DamL2Bal", "Craft_Upgrade_DurL2Bal", "Craft_Upgrade_DurL2Dam", "Craft_Upgrade_BalL2Dam",
    "Craft_Upgrade_BalL2Dur", "Craft_Upgrade_DamL2DurL2BalL2_Clicker", "Craftplan_MedKit_Large_Healing",
    "Craftplan_MedKit_Large_Natural", "Craftplan_Lockpick", "Craftplan_FireCrackers", "Craftplan_ThrowableWater",
    "Craftplan_ThrowableFuel", "Craftplan_Shuriken", "Craftplan_ThrowingKnife", "Craftplan_Molotov",
    "Craftplan_Flare", "Craftplan_Bomb", "Craftplan_NailBomb", "Craftplan_BurningShuriken",
    "Craftplan_ExplodingShuriken", "Craftplan_FreezingShuriken", "Craftplan_PoisonMelee", "Craftplan_BleedMelee",
    "Craftplan_ElectricMelee", "Craftplan_BurnMelee", "Craftplan_BlastMelee", "Craftplan_AntPotion",
    "Craftplan_HyenaPotion", "Craftplan_WolfPotion", "Craftplan_TarantulaPotion", "Craftplan_Cloud9",
    "Craftplan_PoisonPen", "Craftplan_Dentist", "Craftplan_StinkyEdge", "Craftplan_PuffPuffPass",
    "Craftplan_PoisonStrapon", "Craftplan_AirportSecurity", "Craftplan_WaterCurrent", "Craftplan_Electrician",
    "Craftplan_Electrocutioner", "Craftplan_Tazer", "Craftplan_TruActionElectricBaseball", "Craftplan_ShortCircuit",
    "Craftplan_ZombieClassic", "Craftplan_Zazhigalka", "Craftplan_Welder", "Craftplan_FlameBlade",
    "Craftplan_PocketLighter", "Craftplan_HeavyWelder", "Craftplan_SpikedCollar", "Craftplan_GetMedieval",
    "Craftplan_Barbershop", "Craftplan_FlapClap", "Craftplan_CattleStamp", "Craftplan_Rooster",
    "Craftplan_HomeRun", "Craftplan_GTFO", "Craftplan_StayDown", "Craftplan_CutNGo", "Craftplan_FreezeBomb",
    "Craftplan_PoisonBomb", "Craftplan_PoisonFireCrackers", "Craftplan_BombFireCrackers",
    "Craftplan_NailsFireCrackers", "Craftplan_PukeNNuke", "Craftplan_BadHangover", "Craftplan_FilthyBlade",
    "Craftplan_FireLauncher", "Craftplan_GTFO20", "Craftplan_BadAss", "Craftplan_GlowingStick",
    "Craftplan_GrillemAndKillem", "Craftplan_Zappo", "Craftplan_SurpriseMFs", "Craftplan_ThornCrown",
    "Craftplan_HolyGhost", "Craftplan_ElectriCutter", "Craftplan_ToxicReaper", "Craftplan_PoisonBlast",
    "Craftplan_GodHammer", "Craftplan_AngelSword", "Craftplan_AllInOne", "Craftplan_LightingRod",
    "Craftplan_Cloak_Prime", "Craftplan_Poison_Prime", "Craftplan_GhulPotion", "Craftplan_ImpactShield",
    "Craftplan_ElectricShield", "Craftplan_FreezeShield", "Craftplan_Cloak_Mushrooms", "Craftplan_Cloak_Goon",
    "Craftplan_Cloak_Bomber", "Craftplan_KurtBomb", "Craftplan_MedKit_Algae", "Craftplan_ZaidFlare",
    "Craftplan_Shield", "zzz_Craftplan_Bow", "zzz_Craftplan_Arrow", "zzz_Craftplan_ArrowBurn",
    "zzz_Craftplan_ArrowElectric", "zzz_Craftplan_ArrowExploding", "ZZZZ3_Craftplan_Crossbow",
    "ZZZZ3_Craftplan_UpgradedCrossbow", "ZZZZ3_Craftplan_CrossbowBolt", "ZZZZ3_Craftplan_CrossbowBolt_Poison",
    "ZZZZ3_Craftplan_CrossbowBolt_Stunning", "ZZZZ3_Craftplan_CrossbowBolt_Impact", "ZZZZ3_Craftplan_HelluvaHomeRun",
    "ZZZZ3_Craftplan_DevilStick", "ZZZZ3_Craftplan_HotSwing", "ZZZZ3_Craftplan_MagmaEdge",
    "ZZZZ3_Craftplan_ScorchingSummer", "ZZZZ3_Craftplan_FlameStabber", "ZZZZ3_Craftplan_RoastBlast",
    "ZZZZ3_Craftplan_HeavyVenom", "ZZZZ3_Craftplan_CountrysideBane", "ZZZZ3_Craftplan_CobraSting",
    "ZZZZ3_Craftplan_DirtyTool", "ZZZZ3_Craftplan_DrippingEdge", "ZZZZ3_Craftplan_Toxinator",
    "ZZZZ3_Craftplan_ColdCop", "ZZZZ3_Craftplan_StiffStick", "ZZZZ3_Craftplan_ChillKill",
    "ZZZZ3_Craftplan_NorthPole", "ZZZZ3_Craftplan_IceCream", "ZZZZ3_Craftplan_FrostBite",
    "ZZZZ3_Craftplan_IceBerg", "ZZZZ3_Craftplan_BigThunder", "ZZZZ3_Craftplan_ElectroTool",
    "ZZZZ3_Craftplan_BadPlug", "ZZZZ3_Craftplan_PortableCharger", "ZZZZ3_Craftplan_SuperNova",
    "ZZZZ3_Craftplan_Discharger", "ZZZZ3_Craftplan_Nailer", "ZZZZ3_Craftplan_Haemorrhage",
    "ZZZZ3_Craftplan_Exsanguinate", "ZZZZ3_Craftplan_Phlebotomizer", "ZZZZ3_Craftplan_Depleter",
    "ZZZZ3_Craftplan_SuperMolotov", "ZZZZ3_Craftplan_WaterDLC", "ZZZZ3_Craftplan_Engine_v1",
    "ZZZZ3_Craftplan_Turbo_v1", "ZZZZ3_Craftplan_Suspension_v1", "ZZZZ3_Craftplan_Tires_v1",
    "ZZZZ3_Craftplan_Brakes_v1", "ZZZZ3_Craftplan_Engine_v2", "ZZZZ3_Craftplan_Turbo_v2",
    "ZZZZ3_Craftplan_Suspension_v2", "ZZZZ3_Craftplan_Tires_v2", "ZZZZ3_Craftplan_Brakes_v2",
    "ZZZZ3_Craftplan_Engine_v3", "ZZZZ3_Craftplan_Turbo_v3", "ZZZZ3_Craftplan_Suspension_v3",
    "ZZZZ3_Craftplan_Tires_v3", "ZZZZ3_Craftplan_Brakes_v3", "ZZZZ3_Craftplan_Engine_v4",
    "ZZZZ3_Craftplan_Turbo_v4", "ZZZZ3_Craftplan_Suspension_v4", "ZZZZ3_Craftplan_Tires_v4",
    "ZZZZ3_Craftplan_Brakes_v4", "ZZZZ3_Craftplan_Engine_v5", "ZZZZ3_Craftplan_Turbo_v5",
    "ZZZZ3_Craftplan_Suspension_v5", "ZZZZ3_Craftplan_Tires_v5", "ZZZZ3_Craftplan_Brakes_v5",
    "ZZZZ3_Craftplan_Engine_v6", "ZZZZ3_Craftplan_Turbo_v6", "ZZZZ3_Craftplan_Suspension_v6",
    "ZZZZ3_Craftplan_Tires_v6", "ZZZZ3_Craftplan_Brakes_v6", "ZZZZ3_Craftplan_Mine",
    "ZZZZ3_Craftplan_MedKit_Large_Algae", "Craftplan_PunkQueen", "Craftplan_BuzzKiller",
    "Craftplan_NightClub", "Craftplan_Lacerator", "Craftplan_TheConstable", "Craftplan_WrenchKiss",
    "Craftplan_Bow_UrbanTrapper", "Craftplan_Arrow_NightHunter", "Craftplan_ArrowBurn_NightHunter",
    "Craftplan_ArrowElectric_NightHunter", "Craftplan_ArrowExploding_NightHunter", "Craftplan_RifleSharpshooter",
    "Craftplan_ShortSwordCNighthunter", "Craftplan_KnifeBNighthunter", "Craftplan_BatonANighthunter",
    "Craftplan_BigHammerANighthunter", "Craftplan_HMR_Gaas", "Craftplan_AddOn_Rifle_Winter",
    "Craftplan_AddOn_Machete_Winter", "Craftplan_AddOn_Knife_Winter", "Craftplan_AddOn_Shotgun_WildWest",
    "Craftplan_AddOn_Revolver_WildWest", "Craftplan_AddOn_Knife_WildWest", "Craftplan_Spanner_Gaas",
    "Craftplan_Gaas_Halloween_Shotgun", "Craftplan_Gaas_Halloween_Sickle", "Craftplan_AddOn_Silenced_PistolA",
    "Craftplan_AddOn_Silenced_PistolB", "Craftplan_Liveops_Christmas_Candy_Crusher", "Craftplan_Dev1",
    "Craftplan_SiCKbomb", "Craftplan_DevRHofgloVA", "Craftplan_DevSquirell", "Craftplan_DevAirStrike",
    "Craftplan_DevExcalibour", "Craftplan_DevKorekMachete", "ZZZ_Craftplan_DevKorekMachete2",
    "zzz2_Craftplan_DevCraft2", "ZZZZ3_Craftplan_DevCraft3", "ZZZZ3_Craftplan_DevCraft4",
    "ZZZZ3_Craftplan_ToyGunTwins", "ZZZZ3_Craftplan_SuperZombieGrenade", "ZZZZ3_Craftplan_SwanLakeGrenade",
    "ZZZZ3_Craftplan_ToyGunTwins_Ammo", "ZZZZZ_Craftplan_DevCraft5"
]

def get_valid_items():
    items = {}
    filepath = "validitemids.txt"
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                match = re.search(r'Item\((\d+),\s*"([^"]+)"\)', line)
                if match:
                    items[match.group(2)] = int(match.group(1))
    return items