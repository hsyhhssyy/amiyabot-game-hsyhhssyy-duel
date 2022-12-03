#!/bin/sh

rm amiyabot-game-hsyhhssyy-duel-*.zip
zip -q -r amiyabot-game-hsyhhssyy-duel-1.2.zip *
rm -rf ../../amiya-bot-v6/plugins/amiyabot-game-hsyhhssyy-duel-*
mv amiyabot-game-hsyhhssyy-duel-*.zip ../../amiya-bot-v6/plugins/
docker restart amiya-bot 