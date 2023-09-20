# HextechButEfficient

🔠League of Legends snippet scripts gathered in GUI for quick &amp; efficient loot (and not only) management in a min-max resources style. I also provide some utility scripts that aren't about loot.

> **Warning**
> Unfortunately, I have not done GUI yet so for now it's only Python scripts that you can run yourself and see the output.

## 📔 Table of Contents

- [HextechButEfficient](#hextechbutefficient)
  - [📔 Table of Contents](#-table-of-contents)
  - [🔵 Champion Shards disenchant accounting for Mastery levels](#-champion-shards-disenchant-accounting-for-mastery-levels)
  - [😈 Remove Challenges Tokens](#-remove-challenges-tokens)
  - [⚙️ Backup/Restore Settings](#️-backuprestore-settings)
  - [🟠 Skins and Skin Shards related statistics/math](#-skins-and-skin-shards-related-statisticsmath)

## 🔵 Champion Shards disenchant accounting for Mastery levels

> **Note**
> This script is located in `be_mastery/` folder

When you upgrade Champion Mastery level you can either spend a champion shard (partial or permanent) or 2400 BE. If you want to be efficient BE-wise you should definitely choose partial champion shard from those (maybe even wait to get it from level-up capsules if you don't have one already). Thus when disenchanting your collection of champion shards for BE Emporium you want to

- keep 2 shards for your level 5 and below champions
- keep 1 shard for your level 6 champions
- and you are free to disenchant all shards for your level 7 champions.
- keep 3 shards for champions you don't own.
- disenchant all permanent shards of champions you own

Now, I can see improvements to this strategy, i.e selecting some champion pool you won't ever grind/play/buy meaning you can freely disenchant those shards too since you declare those to be completely useless. Let's start with general strategy for all.

## 😈 Remove Challenges Tokens

> **Note**
> This script is located in `remove_tokens/` folder

For some reason, you can't deselect Challenge tokens in this menu (please inform me how if it is possible):
![Remove Tokens](./assets/remove_tokens.png)

Well, fortunately, the script does exactly that: remove tokens from your profile - resetting it to a state with 3 empty tokens.

## ⚙️ Backup/Restore Settings

> **Note**
> This script is located in `settings/` folder

Self-explanatory, I guess. Sometimes Riot Client is behaving itself really badly and occasionally it might result in a total wipe out of your settings. It happened to me a few times. You can back-up settings folder or something. But here I backup settings requested from the client itself into `.json` files. There is also restore those settings script.

## 🟠 Skins and Skin Shards related statistics/math

> **Note**
> This script is located in `skin_shards/` folder

If you are buying a lot of event passes or hextech treasures, or abuse friend gifting mystery skin - at some point you start wondering "What's the most efficient way of grinding skins? What's the best strategy?". After a bit you realise that those questions are really difficult to answer if we try to optimize as much as possible. However, let's try our best.

We will need Excel spreadsheet or similar table. And for the math here we would need to know our situation about skins/skin shards loot. The script fetches this info for you to copypaste.
