# 📜 Scrollable Item Grid (SIG) — Message Playbook
## Keel Agent Knowledge Base | SIG Eligibility, Setup, Rules & Process

*Source: Scrollable Item Grid - Message Playbook.pptx (September 2025)*  
*Maintained by: Keel Agent*

---

## 🧭 What Is SIG?

The **Scrollable Item Grid (SIG)** is a below-the-fold (BTF) homepage module that displays:
- A **parent message** as the first card (Card 1)
- **Sub-messages** (Cards 2–6+) from the message hierarchy below it
- Each card contains an item carousel driven by P13N personalization

SIG is a major BTF engagement driver — accounting for **~50% of total BTF engagement** on the homepage.

---

## 📍 ATF vs BTF SIG Strategy

| Placement | What Shows |
|-----------|-----------|
| **Above the Fold (ATF)** | Personalized "Jump Right Back In" → Personalized "Price Drops For You" → Site Merch Tier 1 Messaging |
| **Below the Fold (BTF)** | Site Merch Tier 1 Messaging |

> ⚠️ **Deals Events**: Deals takeover **BOTH** above-the-fold and below-the-fold SIG — no regular Tier 1 SIG during deals events.

> 📌 Personalized modules (Jump Right Back In, Price Drops For You) are **always prioritized** in the SIG module by P13N.

---

## ✅ SIG Message Eligibility Requirements

ALL three must be true:

1. **Tier 1 or Tier 2 message** (not Tier 3/4)
2. **Message hierarchy includes at least 8 relevant messages** (minimum 5 required; 8–12 recommended)
3. **Assortment breadth** within each sub-message to support an item carousel

> 📌 **SIG message selection should be limited** due to operational lift and module performance history.
> 📌 **Not all Tier 1 messages qualify** — they must meet the assortment/message requirements above.

---

## 🏗️ Message & Asset Requirements

### SIG Card 1 — Parent Message
| Requirement | Detail |
|-------------|--------|
| Tier | Must be **Tier 1** message |
| Dedup | Must be **de-duped from HPOV** (can't use same message in both HPOV and SIG) |
| Assets required | **Carousel Heading Asset** + **Item Carousel Asset** |

### SIG Cards 2–6 — Sub-Messages
| Requirement | Detail |
|-------------|--------|
| Quantity | Minimum 5 required; **recommend 8–12** |
| Hierarchy | Must be **direct children** of the parent message in M0→M1 hierarchy |
| Assets required | **Item Carousel Asset** only (no heading asset needed) |

---

## ⚙️ MMUI Setup Requirements

1. **Homepage Eligibility** — message must have Homepage listed in Page Eligibility
2. **Item Carousel**:
   - Minimum of **50 items** to avoid out-of-stocks
   - **Shelf ID recommended** as carousel source
3. **Activated Assets**:
   - Parent Message: "Item Carousel Asset" AND "Carousel Heading Asset"
   - Sub-messages: "Item Carousel Asset" only
4. **MMUI alone is not enough** — you must align with the Homepage team to set up message in the SIG module
5. Setting up in MMUI does NOT automatically show in SIG — requires HP team setup

---

## 🔀 How Personalization Works in SIG

| Element | How Selected |
|---------|-------------|
| **Order of Messages** | Personalized by P13N algorithm based on customer signals |
| **Items shown** | Personalized by P13N algorithm |
| **Priority** | Personalized modules (Jump Right Back In, Price Drops For You) always shown first |

---

## ❓ SIG FAQ

| Question | Answer |
|----------|--------|
| Do all Tier 1 messages need a SIG? | **No** — message owner + editorial owner determine eligibility. Must meet assortment/message requirements. |
| Can I use fewer than 6 sub-messages? | **No** — minimum 6 messages required. Recommend 8+. |
| Can I use the same message in HPOV and SIG? | **No** — deduplication logic prevents this. Contact SCS for workarounds. |
| What assets do I need? | Parent: Carousel Heading Asset + Item Carousel Asset. Sub-messages: Item Carousel Asset only. |
| If MMUI setup is complete, will SIG automatically appear? | **No** — must align with HP team to configure SIG module separately. |
| Who controls message and item order in SIG? | **P13N algorithm** — both order of messages AND items are personalized. |

---

## 🔄 SIG Process — Step-by-Step

1. **Message owner** identifies SIG opportunity
2. **Message owner** maps out recommended SIG message strategy per guardrails
3. **Message owner** connects with SCS team to review proposed SIG strategy
4. **SCS** reviews to ensure SIG message request meets overall guardrails; provides actual message names to support operational needs (e.g., specific message names with "SIG" added)
5. **SCS** shares final SIG message names back with message owner & editorial owner
6. **SCS** adds final SIG message names to monthly calendar doc
7. **Editorial owner** requests carousel header + item carousel assets using final message names
8. **SCS** passes monthly calendar to HP team for HP planning and execution
9. **HP team** includes SIG plans in final review in bi-weekly HP plan doc
10. **Message owner(s)** activate messages and assets prior to launch

> 📌 **Note on ownership**: Message owner will most likely be the C&E M0 message owner given SIG requirements. The Card 1 (parent) owner should coordinate with all sub-message owners for overall SIG execution.

---

## 📋 Active SIG Themes (Nov 2025 – Feb 2026)

| Event | Parent SIG | Sub-Messages |
|-------|-----------|-------------|
| **Thanksgiving/Holiday** | Holiday Gifting SIG | Sub-messages per Dec appendix |
| **Holiday** | Holiday Hosting Must Haves SIG | Per Dec appendix |
| **EOY** | End Of Year Clearance SIG | Per Dec appendix |
| **New Year** | New Year New You SIG | NYNY sub-messages |
| **Valentine's Day** | Valentine's Day SIG | Pre-existing sub-messages |
| **Valentine's Day** | Valentine's Day Gifting SIG | Pre-existing sub-messages |
| **Game Time / Super Bowl** | Game Time SIG | Kitchen Essentials / Appetizers / Food & Bev Rollbacks / Guest Easy Food / NFL Trading Cards / Food & Bev / Disposable Supplies / Party Supplies |
| **Easter** | Easter SIG | Decor / Candy / Baskets / Egg Hunt / Toys |
| **March Savings Event** | March Savings Event SIG | Fashion / Tech / Home / Food / Toys / HH Essentials / Patio / Beauty / Personal Care / Top 100 / New Drop |
| **Mother's Day** | Mother's Day SIG | 10 gift categories |
| **Default (no event)** | Continue Your Shopping (CYS) | Default — always available |

---

## 🔗 SIG in BigQuery

To query SIG-specific performance in `hp_summary_asset`:

```sql
-- SIG module performance
SELECT
  session_start_dt,
  experience_lvl2,
  hp_module_name,
  message_name,
  SUM(module_view_count) AS sig_impressions,
  SUM(asset_clicks_count) AS sig_clicks,
  SAFE_DIVIDE(SUM(asset_clicks_count), SUM(module_view_count)) AS ctr
FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  AND LOWER(hp_module_name) LIKE '%scrollable%'   -- or filter on moduletype
  AND experience_lvl2 IN ('App: iOS', 'App: Android')
GROUP BY 1, 2, 3, 4
ORDER BY sig_impressions DESC
```

> 📌 Use `sov_hp_carousel_content` for SIG SOV analysis by message/sub-message

---

*Last updated by Keel Agent | Source: Scrollable Item Grid - Message Playbook.pptx (September 2025)*
