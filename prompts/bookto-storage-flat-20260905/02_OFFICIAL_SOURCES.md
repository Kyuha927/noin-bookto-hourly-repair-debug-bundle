# Official APFS sources for independent review

Access was checked on 2026-09-05. The reviewer should open the current pages and cite the exact current text rather than relying only on the summaries below.

1. Apple Platform Security, “Role of Apple File System”

   https://support.apple.com/guide/security/role-of-apple-file-system-seca6147599e/web

   Establishes APFS copy-on-write behavior, space sharing, cloning, snapshots, and startup-volume roles including Data and VM.

2. Disk Utility User Guide, “Get detailed information about a disk”

   https://support.apple.com/guide/disk-utility/get-detailed-information-about-a-disk-dskutl1005/mac

   Describes device, container, volume, capacity, mount-point, and available-space information shown by Disk Utility.

3. Disk Utility User Guide, “View APFS snapshots”

   https://support.apple.com/guide/disk-utility/view-apfs-snapshots-dskuf82354dc/mac

   Defines an APFS snapshot as a read-only copy of its parent APFS volume and describes snapshot information available in Disk Utility.

4. Apple Developer Documentation, “About Apple File System”

   https://developer.apple.com/documentation/foundation/about-apple-file-system

   Provides Apple’s developer-level description of APFS features, including clones and shared free space.

These sources explain filesystem semantics. They do not establish what retained blocks or concurrent writers existed in this incident; that requires matched local measurement.
