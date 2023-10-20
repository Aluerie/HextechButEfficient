# HextechButEfficient

🔠League of Legends [LCU API](<https://riot-api-libraries.readthedocs.io/en/latest/lcu.html>) scripts for quick &amp; efficient management of some chores in a min-max style.

> **Warning**
> Unfortunately, I have not done GUI yet so for now it's only Python scripts that you can run yourself and see the output.

No more annoying animations, no more chore calculations, no more chore lookups in other tab like "do I have mastery 7 on that champ?". Say "No more" to any inefficiency.

## 📔 Table of Contents

- [HextechButEfficient](#hextechbutefficient)
  - [📔 Table of Contents](#-table-of-contents)
  - [📃 List of Scripts](#-list-of-scripts)
    - [🔵 Efficient BE (Blue Essence) management](#-efficient-be-blue-essence-management)
    - [🟠 Efficient OE (Orange Essence) management](#-efficient-oe-orange-essence-management)
    - [🤯 Misc](#-misc)
    - [🪓 Final Chore minimisation](#-final-chore-minimisation)
    - [😈 Remove Challenges Tokens](#-remove-challenges-tokens)
    - [⚙️ Backup/Restore Settings](#️-backuprestore-settings)
    - [💎 Skins and Skin Shards related statistics/math](#-skins-and-skin-shards-related-statisticsmath)
    - [🚢 Event Pass](#-event-pass)
  - [🪚 Ideas and Contributions](#-ideas-and-contributions)
  - [👊 Riot Games Approval](#-riot-games-approval)
  - [⚠️ No Personal Responsibility Disclaimer](#️-no-personal-responsibility-disclaimer)
  - [🌗 Last Note](#-last-note)

## 📃 List of Scripts

### 🔵 Efficient BE (Blue Essence) management

- [X] Mass-Disenchant Champion Shards accounting for Mastery levels.
- [ ] Mass-Open BE related loot.
- [ ] Upgrade Champion Mastery if available.

### 🟠 Efficient OE (Orange Essence) management

- [ ] Mass-Disenchant everything that gives OE.
- [ ] Mass-Open OE related loot.
- [ ] Waste all OE to upgrade the cheapest skin shards.
- [X] Show skin shards for champions without a skin.

### 🤯 Misc

- [ ] Combine Key Fragments.
- [ ] Remove `isNew` shining (that you need to hover over to remove).

### 🪓 Final Chore minimisation

- [ ] Construct your own chore out of available scripts, gather it all in just one button and even schedule it.

### 😈 Remove Challenges Tokens

Unfortunately, you can't deselect Challenge tokens in the 'Customize identity' menu.

- [X] Fortunately, the script does exactly that: resets your profile to a state with 3 empty tokens.

### ⚙️ Backup/Restore Settings

Sometimes League Client behaves itself really badly and occasionally it might result in a total wipe out of your settings. It happened to me a few times when I was nerding too hard. Yes, you can just back-up settings folder in installation directory or something. But here are some scripts:

- [X] Export (backup) settings to `.json` files.
- [X] Import (restore) settings from `.json` files.

### 💎 Skins and Skin Shards related statistics/math

If you buy a lot of event passes and spend all tokens on skin orbs - at some point you start wondering: "What's the most efficient way of grinding the skins collection (let it be all skins, subset of your favourite skins or just only one desired skin)? What's the best strategy?" Idk if the answer actually exists but we can try to optimize some metrics and look probabilities. We will need Excel spreadsheet and the data from the provided scripts. However, I'm not ready to share the excel file yet as I'm not sure what format would be best for public.

The scripts here:

- [X] Prints statistic about your skin collection. Number of owned/not-owned skins per RP price tier.
- [X] Same^ for shards loot.

### 🚢 Event Pass

- [ ] Claim all rewards.
- [ ] Buy all skin orbs with a limit.

## 🪚 Ideas and Contributions

Feel free to make contributions, reach me with your ideas and suggestions, report bugs, etc.

## 👊 Riot Games Approval

Sorry, I'm yet to send a request for approval (all things that use LCU API are recommended to be certified by Riot) - I want to make GUI first.

Either way, it's more of a formality, you will not get banned for using this tool/scripts. Many similar applications that also use LCU API with different purposes already exist and have no problems. Honourable mention: [HextechButBetter](https://github.com/MaciejGorczyca/HextechButBetter) repository.

## ⚠️ No Personal Responsibility Disclaimer

I am not to be held responsible for any losses, mistakes and "mistakes", or bugs that can lead to unfortunate situations. Use/modify my scripts on your own risk. Well, I mean, they should be fine, but still, if anything happens - I won't be able to refund those shards back or something.

## 🌗 Last Note

Not sure if I like the name `HextechButEfficient` because we have some non-loot scripts too. Not sure if wordplay of famous [HextechButBetter](https://github.com/MaciejGorczyca/HextechButBetter) project is a fine idea too. If you have any suggestions - please, hit me up.
