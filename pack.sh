#!/bin/sh

zip -q -r amiyabot-game-hsyhhssyy-duel-1.0.zip *
rm -rf ../../amiya-bot-v6/plugins/amiyabot-game-hsyhhssyy-duel-1_0
mv amiyabot-game-hsyhhssyy-duel-1.0.zip ../../amiya-bot-v6/plugins/
docker restart amiya-bot 