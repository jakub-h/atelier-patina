// =====================================================================
//  SITE CONFIG – edit this file to change contacts across the whole site
// =====================================================================
//
// Phone numbers are written in "+420 123 456 789" format. Links (tel:,
// WhatsApp) are derived from them automatically.
//
// VACATION MODE
//   1. Set vacation.active to true.
//   2. Fill in vacation.phone (who to call meanwhile) and optionally
//      vacation.until (shown as "Jsme na dovolené do ...").
//   3. Commit & push. To end vacation, set active back to false.
//
// While vacation is active, vacation.phone replaces the main phone
// everywhere (footer, contact page, WhatsApp links) and a notice is
// shown on the contact page.

window.SITE_CONFIG = {
  phone: "+420 608 647 151",

  vacation: {
    active: false,
    until: "",              // e.g. "20. října" – leave empty to hide the date
    phone: "+420 608 654 171" // number to call during vacation; "" = email only
  }
};
