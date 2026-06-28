-- ============================================================
-- Battle Pass System - player table migration
-- Adds columns required by ENABLE_BATTLEPASS_SYSTEM
-- ============================================================

ALTER TABLE `player`
    ADD COLUMN `battlepass_daily_missions` BLOB NOT NULL DEFAULT '' BEFORE `quickslot`,
    ADD COLUMN `battlepass_weekly_missions` BLOB NOT NULL DEFAULT '' BEFORE `quickslot`,
    ADD COLUMN `battlepass_player_data` BLOB NOT NULL DEFAULT '' BEFORE `quickslot`;