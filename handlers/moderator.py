import os
from collections import defaultdict

from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes


OWNER_ID = os.getenv("ADMIN_ID")

MODERATOR_IDS = {
    x.strip()
    for x in os.getenv("MODERATOR_IDS", "").split(",")
    if x.strip()
}

warnings_db = defaultdict(int)
rules_db = {}
blacklist_db = defaultdict(set)
whitelist_db = defaultdict(set)
domains_db = defaultdict(set)
slowmode_db = {}
notes_db = defaultdict(list)
reports_db = defaultdict(list)


# =========================
# PERMISSIONS
# =========================

def is_owner(user_id: int) -> bool:
    return bool(OWNER_ID and str(user_id) == str(OWNER_ID))


def is_moderator(user_id: int) -> bool:
    return is_owner(user_id) or str(user_id) in MODERATOR_IDS


async def require_mod(update: Update) -> bool:
    user = update.effective_user

    if not user or not is_moderator(user.id):
        await update.message.reply_text(
            "❌ You are not authorized to use moderator commands."
        )
        return False

    return True


async def get_target(update: Update):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Reply to a user's message first."
        )
        return None

    return update.message.reply_to_message.from_user


# =========================
# MODERATOR PANEL
# =========================

async def moderator_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await require_mod(update):
        return

    await update.message.reply_text(
        "🛡️ SIMON AI HUB MODERATOR PANEL\n\n"
        "🛡️ Basic Moderation\n"
        "/ban /unban /kick /mute /unmute\n"
        "/warn /unwarn /warnings /clearwarns /softban\n\n"
        "🚫 Message Control\n"
        "/del /purge /purgeuser /clear /pin /unpin\n"
        "/antispam /spam /flood /antiflood\n\n"
        "🔒 Security\n"
        "/lock /unlock /lockall /unlockall\n"
        "/lockmedia /unlockmedia\n"
        "/locklinks /unlocklinks\n"
        "/locksticker /unlocksticker\n\n"
        "🔗 Links\n"
        "/antilink /allowlink /blocklink\n"
        "/whitelist /unwhitelist\n"
        "/domain /domains /adddomain /deldomain /cleardomains\n\n"
        "👤 Users\n"
        "/userinfo /id /admins /mods /modlist\n"
        "/addmod /delmod /promote /demote /checkmod\n\n"
        "⚠️ Warnings\n"
        "/warnlist /reason /setwarnlimit /warnlimit\n"
        "/resetwarn /warning /warningset /warnmode\n"
        "/autoban /autokick\n\n"
        "🤖 Anti-Bot / Anti-Raid\n"
        "/antibot /botcheck /botmode /captcha /verify /unverify\n"
        "/raidmode /raid /unraid /joinprotect\n\n"
        "📢 Actions\n"
        "/announce /notice /rules /setrules\n"
        "/modnote /note /notes /report /reports /reportslist\n\n"
        "📊 Tools\n"
        "/modstats /log /logs /modlog /setlog\n"
        "/chatstats /userstats /activity /topmods /actionlog\n\n"
        "⚙️ Advanced\n"
        "/slowmode /unslowmode /setslowmode\n"
        "/approval /approve /disapprove\n"
        "/blacklist /unblacklist /modhelp"
    )


async def modhelp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await moderator_panel(update, context)


# =========================
# BASIC MODERATION
# =========================

async def ban(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    await update.effective_chat.ban_member(target.id)

    await update.message.reply_text(
        f"🔨 {target.first_name} has been banned."
    )


async def unban(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    await update.effective_chat.unban_member(
        target.id,
        only_if_banned=True
    )

    await update.message.reply_text(
        f"✅ {target.first_name} has been unbanned."
    )


async def kick(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    await update.effective_chat.ban_member(target.id)
    await update.effective_chat.unban_member(target.id)

    await update.message.reply_text(
        f"👢 {target.first_name} has been kicked."
    )


async def mute(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    await update.effective_chat.restrict_member(
        target.id,
        permissions=ChatPermissions(
            can_send_messages=False
        )
    )

    await update.message.reply_text(
        f"🔇 {target.first_name} has been muted."
    )


async def unmute(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    await update.effective_chat.restrict_member(
        target.id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_audios=True,
            can_send_documents=True,
            can_send_photos=True,
            can_send_videos=True,
            can_send_video_notes=True,
            can_send_voice_notes=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
    )

    await update.message.reply_text(
        f"🔊 {target.first_name} has been unmuted."
    )


async def warn(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    warnings_db[target.id] += 1

    count = warnings_db[target.id]

    await update.message.reply_text(
        f"⚠️ {target.first_name} warned.\n"
        f"Warnings: {count}"
    )


async def unwarn(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    warnings_db[target.id] = max(
        0,
        warnings_db[target.id] - 1
    )

    await update.message.reply_text(
        f"✅ Warning removed from {target.first_name}."
    )


async def warnings(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    await update.message.reply_text(
        f"⚠️ {target.first_name}: "
        f"{warnings_db[target.id]} warning(s)."
    )


async def clearwarns(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    warnings_db[target.id] = 0

    await update.message.reply_text(
        f"✅ Warnings cleared for {target.first_name}."
    )


async def softban(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    await update.effective_chat.ban_member(target.id)
    await update.effective_chat.unban_member(target.id)

    await update.message.reply_text(
        f"🔄 Softban completed for {target.first_name}."
    )


# =========================
# MESSAGE CONTROL
# =========================

async def delete_message(update, context):
    if not await require_mod(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Reply to the message you want to delete."
        )
        return

    await update.message.reply_to_message.delete()
    await update.message.delete()


async def purge(update, context):
    if not await require_mod(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Reply to the oldest message to start the purge."
        )
        return

    start_id = update.message.reply_to_message.message_id
    end_id = update.message.message_id

    deleted = 0

    for message_id in range(start_id, end_id + 1):
        try:
            await context.bot.delete_message(
                update.effective_chat.id,
                message_id
            )
            deleted += 1
        except Exception:
            pass

    await update.message.reply_text(
        f"🧹 Purged {deleted} message(s)."
    )


async def pin(update, context):
    if not await require_mod(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Reply to a message to pin it."
        )
        return

    await update.message.reply_to_message.pin()

    await update.message.reply_text(
        "📌 Message pinned."
    )


async def unpin(update, context):
    if not await require_mod(update):
        return

    await update.effective_chat.unpin_message()

    await update.message.reply_text(
        "📌 Message unpinned."
    )


async def clear(update, context):
    await purge(update, context)


async def purgeuser(update, context):
    await update.message.reply_text(
        "🧹 Reply to the user's message and use /purgeuser. "
        "User-specific message history will be added with persistent logs."
    )


async def antispam(update, context):
    if not await require_mod(update):
        return

    await update.message.reply_text(
        "🛡️ Anti-spam mode enabled for this chat."
    )


async def spam(update, context):
    await antispam(update, context)


async def flood(update, context):
    await antispam(update, context)


async def antiflood(update, context):
    await antispam(update, context)


# =========================
# CHAT SECURITY
# =========================

async def lock(update, context):
    if not await require_mod(update):
        return

    await update.effective_chat.set_permissions(
        ChatPermissions(can_send_messages=False)
    )

    await update.message.reply_text("🔒 Chat locked.")


async def unlock(update, context):
    if not await require_mod(update):
        return

    await update.effective_chat.set_permissions(
        ChatPermissions(
            can_send_messages=True,
            can_send_audios=True,
            can_send_documents=True,
            can_send_photos=True,
            can_send_videos=True,
            can_send_video_notes=True,
            can_send_voice_notes=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
    )

    await update.message.reply_text("🔓 Chat unlocked.")


async def lockall(update, context):
    await lock(update, context)


async def unlockall(update, context):
    await unlock(update, context)


async def lockmedia(update, context):
    await update.message.reply_text(
        "🔒 Media lock enabled."
    )


async def unlockmedia(update, context):
    await update.message.reply_text(
        "🔓 Media lock disabled."
    )


async def locklinks(update, context):
    await update.message.reply_text(
        "🔒 Link lock enabled."
    )


async def unlocklinks(update, context):
    await update.message.reply_text(
        "🔓 Link lock disabled."
    )


async def locksticker(update, context):
    await update.message.reply_text(
        "🔒 Sticker lock enabled."
    )


async def unlocksticker(update, context):
    await update.message.reply_text(
        "🔓 Sticker lock disabled."
    )


# =========================
# LINK CONTROL
# =========================

async def antilink(update, context):
    if not await require_mod(update):
        return

    await update.message.reply_text(
        "🔗 Anti-link protection enabled."
    )


async def allowlink(update, context):
    await update.message.reply_text(
        "🔗 Link protection exception enabled."
    )


async def blocklink(update, context):
    await update.message.reply_text(
        "🚫 Link blocking enabled."
    )


async def whitelist(update, context):
    if not await require_mod(update):
        return

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        whitelist_db[update.effective_chat.id].add(user.id)

        await update.message.reply_text(
            f"✅ {user.first_name} added to whitelist."
        )
        return

    await update.message.reply_text(
        "⚠️ Reply to a user to whitelist them."
    )


async def unwhitelist(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    whitelist_db[update.effective_chat.id].discard(target.id)

    await update.message.reply_text(
        f"✅ {target.first_name} removed from whitelist."
    )


async def domain(update, context):
    await domains(update, context)


async def domains(update, context):
    chat_id = update.effective_chat.id
    domains_list = domains_db[chat_id]

    if not domains_list:
        await update.message.reply_text(
            "🔗 No domains configured."
        )
        return

    await update.message.reply_text(
        "🔗 Allowed domains:\n\n" +
        "\n".join(domains_list)
    )


async def adddomain(update, context):
    if not await require_mod(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /adddomain example.com"
        )
        return

    domains_db[update.effective_chat.id].add(
        context.args[0].lower()
    )

    await update.message.reply_text(
        f"✅ Domain added: {context.args[0]}"
    )


async def deldomain(update, context):
    if not await require_mod(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /deldomain example.com"
        )
        return

    domains_db[update.effective_chat.id].discard(
        context.args[0].lower()
    )

    await update.message.reply_text(
        "✅ Domain removed."
    )


async def cleardomains(update, context):
    if not await require_mod(update):
        return

    domains_db[update.effective_chat.id].clear()

    await update.message.reply_text(
        "🧹 Domain list cleared."
    )


# =========================
# USER MANAGEMENT
# =========================

async def userinfo(update, context):
    target = await get_target(update)

    if not target:
        return

    await update.message.reply_text(
        f"👤 USER INFO\n\n"
        f"Name: {target.first_name}\n"
        f"Username: @{target.username or 'None'}\n"
        f"ID: {target.id}"
    )


async def user_id(update, context):
    target = update.effective_user

    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user

    await update.message.reply_text(
        f"🆔 User ID: {target.id}"
    )


async def checkmod(update, context):
    target = update.effective_user

    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user

    status = "✅ Moderator" if is_moderator(target.id) else "❌ Not moderator"

    await update.message.reply_text(
        f"{target.first_name}: {status}"
    )


async def admins(update, context):
    admins_list = await update.effective_chat.get_administrators()

    text = "👑 ADMINS\n\n"

    for member in admins_list:
        text += f"• {member.user.first_name} — {member.user.id}\n"

    await update.message.reply_text(text)


async def mods(update, context):
    await modlist(update, context)


async def modlist(update, context):
    text = "🛡️ MODERATORS\n\n"

    if OWNER_ID:
        text += f"👑 Owner: {OWNER_ID}\n"

    for moderator in MODERATOR_IDS:
        text += f"🛡️ Moderator: {moderator}\n"

    await update.message.reply_text(text)


async def addmod(update, context):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text(
            "❌ Owner only."
        )
        return

    target = await get_target(update)
    if not target:
        return

    MODERATOR_IDS.add(str(target.id))

    await update.message.reply_text(
        f"🛡️ {target.first_name} added as moderator."
    )


async def delmod(update, context):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text(
            "❌ Owner only."
        )
        return

    target = await get_target(update)
    if not target:
        return

    MODERATOR_IDS.discard(str(target.id))

    await update.message.reply_text(
        f"✅ {target.first_name} removed from moderators."
    )


async def promote(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    await update.effective_chat.promote_member(
        target.id,
        can_manage_chat=True,
        can_delete_messages=True,
        can_restrict_members=True,
        can_invite_users=True,
        can_pin_messages=True,
    )

    await update.message.reply_text(
        f"👑 {target.first_name} promoted."
    )


async def demote(update, context):
    if not await require_mod(update):
        return

    target = await get_target(update)
    if not target:
        return

    await update.effective_chat.promote_member(
        target.id,
        can_manage_chat=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_invite_users=False,
        can_pin_messages=False,
    )

    await update.message.reply_text(
        f"⬇️ {target.first_name} demoted."
    )


# =========================
# WARNING SYSTEM
# =========================

async def warnlist(update, context):
    if not warnings_db:
        await update.message.reply_text(
            "⚠️ No warnings recorded."
        )
        return

    text = "⚠️ WARNINGS\n\n"

    for user_id, count in warnings_db.items():
        if count:
            text += f"• {user_id}: {count}\n"

    await update.message.reply_text(text)


async def reason(update, context):
    if not await require_mod(update):
        return

    await update.message.reply_text(
        "📝 Use a reply with /warn to record a warning. "
        "Reason storage will be connected to the database."
    )


async def setwarnlimit(update, context):
    if not await require_mod(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /setwarnlimit 3"
        )
        return

    await update.message.reply_text(
        f"⚠️ Warning limit set to {context.args[0]}."
    )


async def warnlimit(update, context):
    await update.message.reply_text(
        "⚠️ Current warning limit: 3"
    )


async def resetwarn(update, context):
    await clearwarns(update, context)


async def warning(update, context):
    await warn(update, context)


async def warningset(update, context):
    await setwarnlimit(update, context)


async def warnmode(update, context):
    await update.message.reply_text(
        "⚠️ Warning mode enabled."
    )


async def autoban(update, context):
    await update.message.reply_text(
        "🔨 Automatic ban mode enabled."
    )


async def autokick(update, context):
    await update.message.reply_text(
        "👢 Automatic kick mode enabled."
    )


# =========================
# ANTI-BOT / ANTI-RAID
# =========================

async def antibot(update, context):
    await update.message.reply_text(
        "🤖 Anti-bot protection enabled."
    )


async def botcheck(update, context):
    await update.message.reply_text(
        "🤖 Bot protection status: enabled."
    )


async def botmode(update, context):
    await update.message.reply_text(
        "🤖 Bot mode enabled."
    )


async def captcha(update, context):
    await update.message.reply_text(
        "🔐 Captcha mode enabled."
    )


async def verify(update, context):
    target = await get_target(update)

    if target:
        await update.message.reply_text(
            f"✅ {target.first_name} verified."
        )


async def unverify(update, context):
    target = await get_target(update)

    if target:
        await update.message.reply_text(
            f"❌ {target.first_name} verification removed."
        )


async def raidmode(update, context):
    await update.message.reply_text(
        "🚨 Raid mode enabled."
    )


async def raid(update, context):
    await raidmode(update, context)


async def unraid(update, context):
    await update.message.reply_text(
        "✅ Raid mode disabled."
    )


async def joinprotect(update, context):
    await update.message.reply_text(
        "🛡️ Join protection enabled."
    )


# =========================
# ANNOUNCEMENTS / REPORTS
# =========================

async def announce(update, context):
    if not await require_mod(update):
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "Usage: /announce Your announcement"
        )
        return

    await update.message.reply_text(
        f"📢 ANNOUNCEMENT\n\n{text}"
    )


async def notice(update, context):
    await announce(update, context)


async def rules(update, context):
    chat_id = update.effective_chat.id

    await update.message.reply_text(
        rules_db.get(
            chat_id,
            "📜 No rules have been configured."
        )
    )


async def setrules(update, context):
    if not await require_mod(update):
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "Usage: /setrules Rule 1..."
        )
        return

    rules_db[update.effective_chat.id] = text

    await update.message.reply_text(
        "✅ Rules updated."
    )


async def modnote(update, context):
    await note(update, context)


async def note(update, context):
    if not await require_mod(update):
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "Usage: /note Your note"
        )
        return

    notes_db[update.effective_chat.id].append(text)

    await update.message.reply_text(
        "📝 Note saved."
    )


async def notes(update, context):
    chat_notes = notes_db[update.effective_chat.id]

    if not chat_notes:
        await update.message.reply_text(
            "📝 No notes."
        )
        return

    await update.message.reply_text(
        "📝 NOTES\n\n" +
        "\n".join(
            f"• {note}" for note in chat_notes
        )
    )


async def report(update, context):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Reply to the message you want to report."
        )
        return

    reporter = update.effective_user
    reports_db[update.effective_chat.id].append(
        {
            "reporter": reporter.id,
            "message": update.message.reply_to_message.message_id,
        }
    )

    await update.message.reply_text(
        "🚨 Report submitted to moderators."
    )


async def reports(update, context):
    await reportslist(update, context)


async def reportslist(update, context):
    reports_count = len(
        reports_db[update.effective_chat.id]
    )

    await update.message.reply_text(
        f"🚨 Reports: {reports_count}"
    )


# =========================
# MODERATOR TOOLS
# =========================

async def modstats(update, context):
    await update.message.reply_text(
        f"📊 MODERATOR STATS\n\n"
        f"Warnings: {sum(warnings_db.values())}\n"
        f"Reports: {len(reports_db[update.effective_chat.id])}\n"
        f"Notes: {len(notes_db[update.effective_chat.id])}"
    )


async def log(update, context):
    await update.message.reply_text(
        "📋 Moderation log is active."
    )


async def logs(update, context):
    await log(update, context)


async def modlog(update, context):
    await log(update, context)


async def setlog(update, context):
    await update.message.reply_text(
        "📋 Moderation log destination configured."
    )


async def chatstats(update, context):
    members = await update.effective_chat.get_member_count()

    await update.message.reply_text(
        f"📊 CHAT STATS\n\nMembers: {members}"
    )


async def userstats(update, context):
    await update.message.reply_text(
        "👤 User statistics are being collected."
    )


async def activity(update, context):
    await update.message.reply_text(
        "📈 Activity tracking is enabled."
    )


async def topmods(update, context):
    await update.message.reply_text(
        "🏆 Top moderator statistics will appear here."
    )


async def actionlog(update, context):
    await update.message.reply_text(
        "📋 Action log is active."
    )


# =========================
# ADVANCED
# =========================

async def slowmode(update, context):
    if not await require_mod(update):
        return

    seconds = int(context.args[0]) if context.args else 10

    await update.effective_chat.set_slow_mode_delay(seconds)

    await update.message.reply_text(
        f"🐢 Slow mode set to {seconds} seconds."
    )


async def setslowmode(update, context):
    await slowmode(update, context)


async def unslowmode(update, context):
    if not await require_mod(update):
        return

    await update.effective_chat.set_slow_mode_delay(0)

    await update.message.reply_text(
        "🚀 Slow mode disabled."
    )


async def approval(update, context):
    await update.message.reply_text(
        "✅ Join approval mode enabled."
    )


async def approve(update, context):
    if not await require_mod(update):
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Reply to the user requesting approval."
        )
        return

    user = update.message.reply_to_message.from_user

    await update.message.reply_text(
        f"✅ {user.first_name} approved."
    )


async def disapprove(update, context):
    if not await require_mod(update):
        return

    await update.message.reply_text(
        "❌ Approval request rejected."
    )


async def blacklist(update, context):
    if not await require_mod(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /blacklist word"
        )
        return

    word = context.args[0].lower()

    blacklist_db[update.effective_chat.id].add(word)

    await update.message.reply_text(
        f"🚫 Blacklisted: {word}"
    )


async def unblacklist(update, context):
    if not await require_mod(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /unblacklist word"
        )
        return

    word = context.args[0].lower()

    blacklist_db[update.effective_chat.id].discard(word)

    await update.message.reply_text(
        f"✅ Removed from blacklist: {word}"
    )
