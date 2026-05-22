The process for maintainers.

Search the Git history for commits beginning with "Prepare" for examples.

1.  Try to give any downstreams (Web, iPad) a heads-up in advance.
1.  Ensure 'release' and 'master' branches are clean of local changes and up-to-date with the remote.
1.  If minor-level version (changing Y in X.Y.Z):
    1.  Merge 'release' into 'master'.
    1.  Remove all uses of `BROGUE_VERSION_ATLEAST`.
1.  Reset the 'gha-build' branch to 'release' and check out 'gha-build'. (Our GitHub Actions are configured to always build the 'gha-build' in release mode, so this is how we'll get the release builds.)
1.  Update version numbers in:
    - Rogue.h
    - Info.plist
    - the variants Globals files; each should be incremented with the same policy as the Brogue main mode
    - the seed catalog preamble in SeedCatalog.c, if the dungeon contents (items or machines) have changed
1.  If minor-level version: Delete test recordings in `test/`.
1.  Add an entry to the top of `CHANGELOG.md` containing the current change files in `changes/`. Look at previous entries and try to follow the format closely. You can run `tools/bullet-points changes/*.md` to process the files into a bulleted list to get you started.
1.  Delete the changes files; `git rm changes/*.md`
1.  Commit all above and push the 'gha-build' branch.
1.  Download artifacts from gha-build Action. Test with `tools/gha-release` or equivalent.
1.  Make version tag `vX.Y` or `vX.Y.Z`.
1.  Merge 'gha-build' into 'release'.
1.  If minor-level version: merge 'master' into 'release'.
1.  Push 'master', 'release', and the tag.
1.  [Make release on GitHub](https://github.com/tmewett/BrogueCE/releases/new).

        {summary}
        
        <details>
        <summary>Changes</summary>
        
        {changelog}
        
        </details>
1.  Post to /r/brogueforum.

        Adventurers,

        An update for Brogue CE is now available!

        [Download for Windows, Mac, and Linux](https://github.com/tmewett/BrogueCE/releases)
        
        {summary}
        
        {changelog}
1.  Post to roguelikes Discord.
1.  If minor-level version: cross-post to /r/roguelikes.
