# Anki True Share
This Anki addon allows you to dynamically share your Anki decks using github.
Anki supports exporting and importing decks, but if you update a deck regularly, you have to export it and send it to everyone who uses it.
Those people need to manually import it to their collection, every time you decide to update the deck.
This is not only prone to errors but also a very time-consuming process.

That's why this addon was created!

# How it works

Anki True Share does all this, but automated. For every deck you decide to share, the addon creates a git directory containing the deck, exported as a CSV file.
Besides giving the user the option to manually sync up or down, two hooks are used to automate even that.
One hook runs when you open Anki, precisely after the collection was loaded, and syncs down, meaning it gathers all changes from github and applies them to your local collection.
The second hook runs every time you sync your collection with the Anki servers and syncs up, meaning it exports all shared decks and pushes them to github if there are changes.

# Usage

For every deck you decide to share you need to create a github repository.
Copy the link for adding a remote to a local repository. It looks like this: `https://github.com/bergziegenmichi/anki_true_sync.git`

Open Anki and go to `True Share > Share deck`. Select the deck and enter the remote URL.

Choose whether to push or pull (explained below) and click ok.

Done!

# Push or Pull

Push means you push your local deck to github, you should use this if you initialize the shared deck. This only works if the repository on github is empty!

Pull means you pull the deck from github, you should use this if someone shares a deck with you. Your local deck is never deleted if you are unsure, select pull.

If you selected push on accident, you can revert to a previous state using github. After doing so, make sure to pull/sync down.

# Things that don't work

- You can get problems if two people edit the deck at the same time. Solving them can require a good amount of git skills if you don't want to lose your changes.

- You probably will never be able to delete a card once in a shared deck. Anki True Sync is only able to add or update notes and deleted ones go unnoticed when syncing down.
When syncing up though, the addon notices the CSV file is missing notes, exports your local deck, containing the deleted notes, and pushes them to github. 
Even the person who deleted the notes from their collection will import them on their next sync down. 

- This entire addon on Windows if you use sub-decks because that meme of an operating system doesn't support colons in filenames. So stop using subdecks, or even better, stop using Windows.

# Setup

Download this project and put everything to `~/.local/share/Anki2/addons21/true_sync/` on Linux. On Windows, I have no clue, but you can get it by going to `Tools > Add-ons > View Files` in Anki.

No setup.py doesn't help you. It creates a few directories and the config file and is executed on startup. 


# Coming features

- Sync decks independently
- A UI to manage shared decks
- More options to configure the addon
- Maybe tackle the problem with deleting cards
- Sharing decks read-only
- Windows...
- Open to ideas!

