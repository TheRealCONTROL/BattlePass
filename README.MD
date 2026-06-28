# Battle Pass System v2

<p align="center">
  <img src="https://i.ibb.co/LzsnmRPT/552c97d2c40f.png" alt="Battle Pass System v2">
</p>


A lightweight, fully configurable, and highly optimized Battle Pass system for Metin2.

This version was designed with performance and simplicity in mind while remaining flexible enough to support future expansions.

---

# Features

### 🎯 Daily & Weekly Missions

* Fully randomized Daily missions.
* Fully randomized Weekly missions.
* Automatic mission refresh.
* Duplicate mission prevention.
* Individual mission reroll support.

---

### ⭐ Battle Pass Progression

* EXP-based leveling system.
* Configurable maximum level.
* Automatic level progression.
* Premium & Free reward tracks.
* Automatic monthly reset.

---

### 🎁 Reward System

* Free rewards.
* Premium rewards.
* Automatic reward claiming.
* Configurable reward tables.

Supports either:

* Single reward table for every month.
* Individual reward tables per month.

Simply change:

```cpp
#define SINGLE_REWARDS_TABLE TRUE
```

---

### 🔥 Mission System

Supports multiple mission types.

Examples:

* Kill monsters
* Destroy Metins
* Complete dungeons
* Collect items
* Fishing
* Mining
* Crafting
* (and easily expandable)

Mission objectives and rewards are fully configurable inside:

```cpp
char_battlepass.h
```

---

### ⚡ Multi Mission Progress

A single action can update every mission of the same type simultaneously.

Example:

If two missions require killing monsters:

* Kill 100 Monsters
* Kill 500 Monsters

Both missions can progress together.

Can be enabled or disabled by changing:

```cpp
#define MULTI_MISSION_PROGRESS TRUE
```

---

### 📅 Automatic Timers

The system automatically handles:

* Daily reset
* Weekly reset
* Monthly Battle Pass reset

No manual intervention required.

---

### 🎲 Randomized Missions

Mission requirements are randomized every reset.

Different EXP rewards are automatically assigned depending on mission difficulty.

---

### 💎 Premium Upgrade

Built-in Premium Battle Pass support.

Players can upgrade their Battle Pass using an item.

---

### ⬆ Instant Level Up

Optional Battle Pass Level-Up item included.

Perfect for shop integration.

---

### 🔄 Mission Reroll

Players can reroll an unfinished mission using a dedicated item.

The new mission is guaranteed not to duplicate another active mission.

---

### ✅ Mission Skip

Allows instantly completing the first unfinished mission.

Useful for premium features or special items.

---

### 📦 Optimized Network Packets

* Packed mission data.
* Packed reward data.
* Minimal packet overhead.
* Reduced unnecessary allocations.

---

### ⚙ Optimized Codebase

The system has been written with performance in mind.

Highlights include:

* Modern C++ implementation.
* Smart use of references.
* Static random number generator.
* Efficient packet construction.
* Reduced unnecessary copies.
* Minimal memory allocations.
* Direct array access where appropriate.
* Clean and maintainable architecture.

---

# Configuration

Most configuration can be done directly inside:

```cpp
char_battlepass.h
```

Including:

* Mission list
* Mission requirements
* EXP values
* Reward tables
* Monthly rewards
* Battle Pass limits

---

# Credits

Developed by **CONTROL**

**Discord**

```
control69
```

For more free and premium Metin2 systems, tools and resources:

🌐 https://pay2win-store.vercel.app/

---

Please keep the original credits if you redistribute this project.
