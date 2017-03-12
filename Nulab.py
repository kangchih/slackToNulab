#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2
from cStringIO import StringIO
file_str = StringIO()

class Nulab:
    NAME = 'kangchih'
    HOST = 'backlogtool.com'
    API_KEY = 'HHpPPAeC07y3O9yOU8XrcxgeIx7BQWAZ1Jtzny8rgan1Fyr8UR99V70dclbaW5lM'
    PROJECT_ID = '41703'
    PRIORIRY_ID = '4'
    ISSUE_TYPE_ID = '179399'

    def __init__(self, name=NAME, host=HOST, apiKey=API_KEY, projectId=PROJECT_ID, priorityId=PRIORIRY_ID, issueTypeId=ISSUE_TYPE_ID):
        self.name = name
        self.host = host
        self.apiKey = apiKey
        self.projectId = projectId
        self.priorityId = priorityId
        self.issueTypeId = issueTypeId

    def addIssue(self, summary):
        print '[addIssue] start to add issue.'

        url = 'https://' + self.name + '.' + self.host + '/api/v2/issues?apiKey=' + self.apiKey
        payload = 'projectId=' + self.projectId + '&summary=' + summary + '&issueTypeId=' + self.issueTypeId + '&priorityId=' + self.priorityId
        headers = {'content-type': "application/x-www-form-urlencoded"}
        print "[addIssue] url=", url
        print "[addIssue] payload=", payload
        result = ''
        try:
            req = urllib2.Request(url, payload, headers)
            response = urllib2.urlopen(req)
            result = str(response.getcode())
        except Exception as e:
            print '[addIssue] error ' + str(e)
            result = str(e)

        return 'Add issue response code: ' + result

    def updateIssue(self, issueKey, summary):
        print '[updateIssue] start to update issue.'

        url = 'https://' + self.name + '.' + self.host + '/api/v2/issues/' + issueKey + '?apiKey=' + self.apiKey
        payload = 'summary=' + summary + '&issueTypeId=' + self.issueTypeId + '&priorityId=' + self.priorityId
        headers = {'content-type': "application/x-www-form-urlencoded"}
        print "[updateIssue] url=", url
        result = ''
        try:
            req = urllib2.Request(url, payload, headers)
            req.get_method = lambda: 'PATCH'  # creates the PATCH method
            response = urllib2.urlopen(req)
            result = str(response.getcode())
        except Exception as e:
            print '[updateIssue] error ' + str(e)
            result = str(e)

        return 'Update issue response code: ' + result


    def delIssue(self, issueKey):
        print '[delIssue] start to delete issue.'

        url = 'https://' + self.name + '.' + self.host + '/api/v2/issues/' + issueKey + '?apiKey=' + self.apiKey
        print "[delIssue] url=", url
        result = ''
        try:
            req = urllib2.Request(url)
            req.get_method = lambda: 'DELETE'  # creates the delete method
            response = urllib2.urlopen(req)
            result = str(response.getcode())
        except Exception as e:
            print '[delIssue] error ' + str(e)
            result = str(e)

        return 'Delete issue response code: ' + result


    def getIssueList(self):
        print '[getIssueList] start to get issues.'
        result = ''
        url = 'https://' + self.name + '.' + self.host + '/api/v2/issues?apiKey=' + self.apiKey
        print "[getIssueList] url=", url
        try:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            info = response.read()
            data = json.loads(info)
            print 'Total Issue:' + str(len(data))
            for item in data:
                print '[issueKey]: ' + item['issueKey'] + '\n[summary]: ' + item['summary'] + '\n[description]: ' \
                      + item['description'] + '\n[issueType]: ' + item['issueType']['name'] + '\n[status]: ' + \
                      item['status']['name']
                result += '[keyId]:' + str(item['keyId']) + '\n[issueKey]: ' + item['issueKey'] + '\n[summary]: ' + item['summary'] + '\n[description]: ' \
                      + item['description'] + '\n[issueType]: ' + item['issueType']['name'] + '\n[status]: ' + \
                      item['status']['name'] + '\n'

        except Exception as e:
            print '[getIssueList] error ' + str(e)
            result = str(e)

        return result
