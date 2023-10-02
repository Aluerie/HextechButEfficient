# HextechButEfficient

🔠League of Legends [LCU API](<https://riot-api-libraries.readthedocs.io/en/latest/lcu.html>) scripts for quick &amp; efficient management of some chores in a min-max style.

> **Warning**
> Unfortunately, I have not done GUI yet so for now it's only Python scripts that you can run yourself and see the output.

No more annoying animations, no more chore calculations, no more chore lookups in other tab like "do I have mastery 7 on that champ?". Say "No more" to any inefficiency.

## 📔 Table of Contents

- [HextechButEfficient](#hextechbutefficient)
  - [📔 Table of Contents](#-table-of-contents)
  - [📃 List of Scripts](#-list-of-scripts)
    - [🔵 Efficient BE-management](#-efficient-be-management)
    - [🟠 Efficient OE-management](#-efficient-oe-management)
    - [🤯 Misc](#-misc)
    - [🪓 Final Chore minimisation](#-final-chore-minimisation)
    - [😈 Remove Challenges Tokens](#-remove-challenges-tokens)
    - [⚙️ Backup/Restore Settings](#️-backuprestore-settings)
    - [💎 Skins and Skin Shards related statistics/math](#-skins-and-skin-shards-related-statisticsmath)
  - [🪚 Ideas and Contributions](#-ideas-and-contributions)
  - [👊 Riot Games Approval](#-riot-games-approval)
  - [⚠️ No Personal Responsibility Disclaimer](#️-no-personal-responsibility-disclaimer)
  - [🌗 Last Note](#-last-note)

## 📃 List of Scripts

### 🔵 Efficient BE-management

This includes:

- [ ] Mass-Disenchant Champion Shards accounting for Mastery levels.
  - [X] keep `3/2/1/0` champion shards depending on their mastery - respectively to `not_owned/5_and_below/6/7` level.
  - [ ] Disenchant permanent shards for owned champions.
- [ ] Mass-Open everything that has BE potential:
  - [ ] Hextech chests
    - [ ] Combine Key Fragments for them
  - [ ] Champion capsules (basic/glorious)
  - [ ] Honour capsules/orbs
  - [ ] Not-permanent random champion shards
  - [ ] etc???
- [ ] Upgrade Champion Mastery if available
- [ ] Upgrade champion shards
  - [ ] Champion shards after price is below 7800
  - [ ] Permanent champion shards
- [ ] (?) Possibility to choose favourite/hated champions so they have different treatment

### 🟠 Efficient OE-management

This includes

- [ ] Open all esports capsules.
- [ ] Mass-Open everything has OE potential:
  - [ ] Hextech chests
    - [ ] Combine Key Fragments for them
  - [ ] Random wards
  - [ ] Eternal capsules
  - [ ] etc???
- [ ] Disenchant all:
  - [ ] emotes
  - [ ] icons
  - [ ] eternals
  - [ ] wards
- [ ] Waste all OE to upgrade the cheapest skin shards.

### 🤯 Misc

- [ ] Remove `isNew` shining in loot tab that you need to hover over the shards to remove.
  - [ ] Select what shining to remove, i.e. shining over champion shards is pointless, but shining over skin shards is useful.

### 🪓 Final Chore minimisation

- [ ] Some memory-script that remembers to do everything ticked like one button to rule them all that would do everything marked like all points from OE management and upgrade champion masteries.

### 😈 Remove Challenges Tokens

- Unfortunately, you can't deselect Challenge tokens in the 'Customize identity' menu.

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

## 🪚 Ideas and Contributions

Feel free to make contributions, reach me with your ideas, report bugs, etc.

## 👊 Riot Games Approval

Sorry, I'm yet to send a request for approval (all things that use LCU API are recommended to be certified by Riot) - I want to make GUI first.

Either way, it's more of a formality, you will not get banned. Many similar applications that also use LCU API with different purposes already exist and have no problems. Honourable mention: [HextechButBetter](https://github.com/MaciejGorczyca/HextechButBetter) repository.

## ⚠️ No Personal Responsibility Disclaimer

I am not to be held responsible for any losses, mistakes and "mistakes", or bugs that can lead to unfortunate situations. Use/modify my scripts on your own risk. Well, I mean, they should be fine, but still, if anything happens - I won't be able to refund those shards back or something.

## 🌗 Last Note

Not sure if I like the name `HextechButEfficient` because we have some non-loot scripts too. Not sure if wordplay of famous [HextechButBetter](https://github.com/MaciejGorczyca/HextechButBetter) project is a fine idea too. If you have any suggestions - please, hit me up.
