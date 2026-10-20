# The hand-in script

When a student hands in a piece of supervision work, the BMS supervisions site sends its Word document to this script, [Code.gs](Code.gs). The script runs in your Google account, as a Google Apps Script web app. It checks the hand-in password, saves the document in a folder in your Google Drive (with a subfolder for each supervision), adds a line about it to a Google Sheet, and sends the site a receipt, which the student sees.

Students don't need a Google account, and they never leave the site. The password is kept only in the script's settings (its *Script properties*), which only you can see. It is never in the code, on the site, or in this repository.

## Setting it up (about ten minutes)

1. Sign in to the Google account whose Drive should receive the work, and go to [script.google.com](https://script.google.com). Press **New project**, and name it (click *Untitled project* at the top), for example *BMS supervisions hand-in*.
2. Delete everything in the editor's `Code.gs`, and paste in the whole of [Code.gs](Code.gs) from this folder. Press **Save** (the disk icon).
3. Optional: in **Project Settings** (the cog on the left), tick *Show "appsscript.json" manifest file in editor*. Then open `appsscript.json` in the editor and replace it with [appsscript.json](appsscript.json) from this folder. This sets the time zone to London and gives the web app its settings.
4. Set the password. In **Project Settings** (the cog), under **Script properties**, press **Add script property**. Enter the property `PASSWORD`, and as its value the hand-in password that you will give the students. Then press **Save script properties**. The Dropbox request's password can be used here too, so that students only need one.
5. Make the folder and the sheet. Back in the **Editor** (`< >` on the left), choose `setup` in the list of functions at the top and press **Run**.
   - The first time, Google asks you to let the script use your Drive and Sheets. Press **Review permissions** and choose your account.
   - If Google says *Google hasn't verified this app*, press **Advanced** and then **Go to BMS supervisions hand-in (unsafe)**. It is your own script, so this is expected.
   - Then press **Allow**.

   The *Execution log* then gives the links to the new folder, *BMS supervision work – handed in*, and to the sheet that lists what is handed in (inside the folder).
6. Publish it. Press **Deploy** (top right), then **New deployment**. Under *Select type* (the cog), choose **Web app**, and set:
   - **Description:** *Hand-in*
   - **Execute as:** *Me*
   - **Who has access:** *Anyone*

   Then press **Deploy**. Copy the **Web app URL**, which ends in `/exec`.
7. Check it: open the address in a private (incognito) window, where you aren't signed in to Google, as your students won't be. It should show `{"ok":true,"service":"BMS supervisions hand-in","version":1,"ready":true}`. If Google asks you to sign in instead, *Who has access* isn't *Anyone*: change it under **Deploy → Manage deployments**.
8. Give the address to the site: put it in `assets/js/config.js`, as `script` under `handIn`, and run `python3 build/make_page.py` (the chapters then say that the essay goes straight to your Google Drive) – or send the address to whoever looks after the site.

**If your Google account is managed by an organisation**, its administrator may not allow web apps that *Anyone* can use. If *Anyone* isn't offered in step 6, ask them, or use a personal Google account.

## Afterwards

- **The work** is in Drive, in *BMS supervision work – handed in*, in a folder for each supervision (*Supervision 1*, *Supervision 2*…). Each file is named after the paper and the student, for example `supervision-1-essay-ada-lovelace.docx`. Its description says who handed it in, when, and how many words it has. Nothing is ever replaced: if the same file is handed in again, it is saved as `… (2).docx`.
- **The sheet**, *BMS supervision work – handed in (list)*, has a line for each hand-in: the time, the supervision, the paper, the student's name and candidate number, the number of words, the file and a link to it, and when it was submitted on the site.
- **To change the password**, change `PASSWORD` in the Script properties. You don't need to deploy again.
- **To change the code**, edit it, then press **Deploy → Manage deployments**, the pencil, *Version: New version*, and **Deploy**. The address stays the same. (A **New deployment** would give it a new address.)
- **A new year:** keep the same script and folder, or run `setup` again after deleting `FOLDER_ID` and `SHEET_ID` from the Script properties, which makes a new folder and sheet.

## What it can do

The script runs as you. It can only do what its code does: when the password is right, save the Word document that comes with a hand-in into the folder, and add a line to the sheet. Anyone with the address can call it, but without the password it saves nothing. After 30 wrong passwords in ten minutes, from anyone, it rests until the ten minutes are over. It only takes Word documents (checked by their contents), of up to 10 MB, and it makes their names safe.

`test/t_handin.js` tests the script in Node, with stand-ins for Google's services (`node test/t_handin.js`).
