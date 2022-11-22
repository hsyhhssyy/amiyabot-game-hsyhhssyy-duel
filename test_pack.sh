#!/bin/sh

zip -q -r amiyabot-game-hsyhhssyy-duel-1.1.zip *
rm -rf ../../amiya-bot-v6/plugins/amiyabot-game-hsyhhssyy-duel-1_1
mv amiyabot-game-hsyhhssyy-duel-1.1.zip ../../amiya-bot-v6/plugins/
docker restart amiya-bot 