#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback
import calendar
import time
from Nulab import Nulab
from datetime import datetime, date, timedelta
from slacker import Slacker

class Slack():
    SLACK_EMOJI = ':nulab:'
    SLACK_BOT_NAME = 'kang.bot'

    SLEEP_TIME_EMPTY_RUNS_MAX = 20 * 5 # 5 minutes without message
    SLEEP_TIME_FAST = 3
    SLEEP_TIME_SLOW = 60
    SLEEP_TIME = SLEEP_TIME_FAST

    def __init__(self, channel, token):
        self.channel = channel
        self.slack = Slacker(token)
        self.fet_ts = time.time()

    def _get_current_epoch(self):
        return calendar.timegm(datetime.utcnow().timetuple())

    def _get_slack_user_name(self, user_id):
        user = ''
        try:
            data = self.slack.users.info(user = user_id)
            is_ok = data.body.get('ok', False)
            user = data.body.get('user', None)
            if not is_ok or not user:
                return ''
        except:
            return ''
        return user.get('name', '')

    def _get_slack_messages(self, ts):

        has_exception = False
        all_messages = []
        ts_ret = ts
        while True:
            pag = {}
            try:
                pag = self.slack.groups.history(
                    channel=self.channel,
                    oldest=str(ts_ret)
                    # count=100
                )
            except Exception as e :
                print "Unexpected error! " + str(e)
                has_exception = True
                break

            if not pag.body.get('ok', False):
                print 'ERROR: failed to fetch channel history'
                has_exception = True
                break

            messages = pag.body.get('messages', '')
            for mess in reversed(messages):
                user = mess.get('user', '')
                text = mess.get('text', '')

                # update timestamp for next fetch
                new_ts = mess.get('ts', ts_ret)
                if new_ts > ts_ret:
                    ts_ret = new_ts

                all_messages.append({
                        "id" : user,
                        "text" : text
                    })
            has_more = pag.body.get('has_more', False)
            if not has_more:
                break

        return (has_exception, all_messages, ts_ret)


    def post_slack_message(self, msg):
        self.slack.chat.post_message(
            channel=self.channel,
            text=msg,
            username=Slack.SLACK_BOT_NAME,
        )

    def start(self):

        last_epoch = self._get_current_epoch()
        ts = time.time()

        while True:

            '''
            perform operation(s)
                - get issues
                - add issue
                - delete issue
                - update issue

            wait until next round
            '''

            try:
                current_epoch = self._get_current_epoch()
                time_lasped = current_epoch - last_epoch
                last_epoch = current_epoch

                # fetch history and process commands
                (has_exception, messages, new_ts) = self._get_slack_messages(ts)
                if has_exception:
                    raise Exception
                ts = new_ts

                for mes in messages:
                    user_id = mes['id']
                    text = mes['text']
                    user_name = self._get_slack_user_name(user_id)
                    if not user_name:
                        # TODO: Exception
                        continue
                    print u"user_id: {0}, name: {1}, text: {2}".format(user_id, user_name, text)

                    # show issue list
                    if text == 'get issues':
                        self.post_slack_message(Nulab().getIssueList())
                        continue

                    # add issue
                    if text[0:10] == 'add issue ':
                        print 'Add issue summary:' + text[10:]
                        summary = text[10:]
                        add = Nulab()
                        self.post_slack_message(add.addIssue(summary))
                        continue

                    # delete issue
                    if text[0:13] == 'delete issue ':
                        print 'Delete issueKey:' + text[13:]
                        issueKey = text[13:]
                        delete = Nulab()
                        self.post_slack_message(delete.delIssue(issueKey))
                        continue

                    # update issue
                    if text[0:13] == 'update issue ':
                        print 'Update issue summary:' + text[13:]
                        # split by space once. Ex: NU-1 This is summary => ['NU-1', 'This is summary']
                        msg = text[13:].split(' ', 1)
                        print 'Update issue msg:' + str(msg)
                        issueKey = msg[0]
                        print 'Update issue issueKey:' + issueKey
                        summary = msg[1]
                        print 'Update issue summary:' + summary

                        update = Nulab()
                        self.post_slack_message(update.updateIssue(issueKey, summary))
                        continue

                self.SLEEP_TIME = self.SLEEP_TIME_FAST

                time.sleep(self.SLEEP_TIME)
            except Exception as e:
                print "Exception: " + str(e)
                traceback.print_exc(file=sys.stdout)
                time.sleep(Slack.SLEEP_TIME_FAST)


if __name__ == '__main__':
    # for channel "nulab"
    SLACK_CHANNEL = 'G4GDQEW1W'
    SLACK_TOKEN = 'xoxp-56444582006-56399653907-152510564273-9d7845b1e4e86c1271cfad2138e2b589'
    nulab = Slack(channel=SLACK_CHANNEL, token=SLACK_TOKEN)
    nulab.start()
