# Firebase + GitHub Pages — One-Time Setup

Estimated time: ~20 minutes. You only do this once.

---

## Part 1 — Create a Firebase project

1. Go to **console.firebase.google.com** and sign in with your Google account.
2. Click **Add project** → name it `ita-prints-market` → continue.
3. Disable Google Analytics (not needed) → **Create project**.
4. In the left sidebar click **Build → Realtime Database**.
5. Click **Create Database** → choose **United States (us-central1)** → **Start in test mode** → Enable.
   - Test mode means anyone can read/write for 30 days. That's fine — switch to locked rules after you confirm everything works (see Part 4).

---

## Part 2 — Get your Firebase config

1. In the Firebase console, click the gear icon ⚙️ (top-left) → **Project settings**.
2. Scroll down to **Your apps** → click **</>** (web app icon) → register app as `market`.
3. Copy the `firebaseConfig` object that appears. It looks like:

```js
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "ita-prints-market.firebaseapp.com",
  databaseURL: "https://ita-prints-market-default-rtdb.firebaseio.com",
  projectId: "ita-prints-market",
  storageBucket: "ita-prints-market.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc..."
};
```

4. Open **`market-app/index.html`** and find the `FIREBASE_CONFIG` block near the top of the `<script>` section. Replace every `PASTE_YOUR_*` value with the real values from above.
5. Do the same in **`market-app/operator/index.html`**.

---

## Part 3 — Set your operator PIN

1. In the Firebase console, go to **Realtime Database** → **Data** tab.
2. Hover over the root `/` → click the **+** button to add a child.
3. Name: `config` → click the **+** on that → add two children:
   - `pin` = `1234` (or whatever 4+ digit PIN you want)
   - `ticketCounter` = `0`
4. Your database now has:
   ```
   /config
     pin: "1234"
     ticketCounter: 0
   ```

---

## Part 4 — Load your products

1. Open **`market-app/operator/index.html`** in your browser (file:// is fine for this step).
2. Enter your PIN → click **Products** tab → click **Load ItaPrints Defaults**.
3. This seeds all 11 products into Firebase. Your brother can add his products the same way from his browser.

---

## Part 5 — Push to GitHub Pages

### First time setup

1. Create a new **public** repo on GitHub — name it `ita-market` (or anything you like).
2. In your terminal, `cd` to the `market-app/` folder:
   ```
   cd ~/Desktop/"Claude Code Projects"/"ITA Prints"/"Farmers Market Automated Order Queue"/market-app
   git init
   git add .
   git commit -m "initial market app"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ita-market.git
   git push -u origin main
   ```
3. In the GitHub repo → **Settings** → **Pages** → Source: **Deploy from a branch** → Branch: `main` / `/ (root)` → **Save**.
4. Wait ~60 seconds. Your URLs are:
   - **Customer form:** `https://YOUR_USERNAME.github.io/ita-market/`
   - **Operator view:** `https://YOUR_USERNAME.github.io/ita-market/operator/`

### Your permanent QR code URL

The customer form URL (`https://YOUR_USERNAME.github.io/ita-market/`) never changes. Print it as a QR code, 3D-print the stand, done.

### Updating the app later

```
git add .
git commit -m "update"
git push
```
GitHub Pages redeploys automatically in ~60 seconds.

---

## Part 6 — Tighten Firebase security rules (after first successful test)

In Firebase console → Realtime Database → Rules tab, replace the default rules with:

```json
{
  "rules": {
    "orders": {
      ".read": true,
      ".write": true
    },
    "products": {
      ".read": true,
      ".write": true
    },
    "config": {
      "ticketCounter": {
        ".read": true,
        ".write": true
      },
      "pin": {
        ".read": true,
        ".write": false
      }
    }
  }
}
```

This lets customers submit orders and read products, but prevents anyone from changing the PIN from the browser.

---

## Day-of-market checklist

- [ ] Laptop charged + phone hotspot ready (backup if venue WiFi is flaky)
- [ ] Open `https://YOUR_USERNAME.github.io/ita-market/operator/` on your laptop
- [ ] Open same URL on your brother's laptop
- [ ] Scan the QR code with your phone to confirm customer form loads
- [ ] Place a test order → confirm it appears on both operator views
- [ ] Confirm SVG downloads correctly when you press Start
- [ ] Confirm est. ready time shows on the customer's confirmation screen

---

## Common issues

| Problem | Fix |
|---|---|
| "PASTE_YOUR_API_KEY" still in code | Replace all `PASTE_YOUR_*` values in both HTML files |
| PIN prompt loops | Check `/config/pin` exists in Firebase Data tab |
| No products showing | Click "Load ItaPrints Defaults" on Products tab |
| SVG font looks wrong in xTool | Font must be installed on your Mac. The SVG uses the original font name exactly (e.g. "Grand Hotel") |
| Customer form shows blank product grid | Firebase /products is empty — load defaults from operator page |
| Orders not updating live | Check browser console for Firebase connection errors; ensure databaseURL is correct |
