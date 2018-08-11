from Linephu.linepy import *
from Linephu.akad.ttypes import *
import time
import timeit


client = LINE()
client.log("Auth Token : " + str(client.authToken))
#client = LINE('email', 'password')

oepoll = OEPoll(client)

MySelf = client.getProfile()
JoinedGroups = client.getGroupIdsJoined()
print("My MID : " + MySelf.mid)

whiteListedMid = ["uadb864b186b1290dd86edb85ca87255d", "u23b3abbf2518782cc270e370d4c73713", "u50057fea961021c1599ff21157a84c43", "udb0d47a9a2f0a29804b0fda72787ce68", "u974b7cd3b88d461e103c92ecf3c990a7", "u260ad7f1ae40ae412594930291222161", "ue6aa8348fc13819fad9c3c20c780c897", "ua0eac1836a6251d2e7a7fb448f5ebbb3", "ub51d2d0bb6ac317c501b60c1bf49e7b5"]

#mymid : ""


def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        if op.param1 not in JoinedGroups:
            if op.param2 in whiteListedMid:
                client.acceptGroupInvitation(op.param1)
                JoinedGroups.append(op.param1)
            else:
                client.acceptGroupInvitation(op.param1)
                JoinedGroups.append(op.param1)
                client.leaveGroup(op.param1)
                JoinedGroups.remove(op.param1)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_INVITE_INTO_GROUP\n\n")
        return


def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    # print op
    try:
        b = open("b.txt", "r")
        blackListedMid = b.readline()
        b.close()
        if op.param2 in blackListedMid:
            try:
                client.kickoutFromGroup(op.param1, [op.param2])
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return


def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        if op.param3 == MySelf.mid:
            hb = open("hb.txt", "r")
            b = open("b.txt", "r")
            halfBlackListedMid = hb.readline()
            blackListedMid = b.readline()
            hb.close()
            b.close()
            if op.param2 not in halfBlackListedMid and op.param3 not in blackListedMid:
                hb = open("hb.txt", "w")
                hb.write(op.param2)
                hb.close()
                client.kickoutFromGroup(op.param1, [op.param2])
            elif op.param2 in halfBlackListedMid:
                b = open("b.txt", "w")
                b.write(op.param2)
                b.close()
                client.kickoutFromGroup(op.param1, [op.param2])
            JoinedGroups.remove(op.param1)
        else:
            if op.param3 in whiteListedMid:
                client.kickoutFromGroup(op.param1, [op.param2])
                group = client.getGroup(op.param1)
                if group.preventedJoinByTicket == True:
                    try:
                        group.preventedJoinByTicket = False
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
                else:
                    try:
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return


def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.toType == 0:
                    print("\n")
                    print("Private Chat Message Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Message : " + msg.text)
                    print("\n")
                    if msg._from in whiteListedMid:
                        if msg.text.startswith("/jgurlx"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                            group = client.getGroup(str1)
                            try:
                                client.reissueGroupTicket(str1)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                        elif msg.text.startswith("/jgurl"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                        if msg.text.startswith("/sm"):
                            str1 = find_between_r(msg.text, "mid: ", " mid")
                            str2 = find_between_r(msg.text, "text: ", " text")
                            client.sendMessage(str1, str2)
                        if msg.text.startswith("/sc"):
                            str1 = find_between_r(msg.text, "mid: ", " mid")
                            str2 = find_between_r(msg.text, "cmid: ", " cmid")
                            client.sendContact(str1, str2)
                        if msg.text.startswith("/kick"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "mid: ", " mid")
                            if str2 not in whiteListedMid:
                                try:
                                    client.kickoutFromGroup(str1, [str2])
                                except Exception as e:
                                    print(e)
                elif msg.toType == 2:
                    if msg._from in whiteListedMid:
                        print("\n")
                        print("Private Chat Message Received")
                        print("Sender's Name : " + client.getContact(msg._from).displayName)
                        print("Sender's MID : " + msg._from)
                        print("Received Message : " + msg.text)
                        print("\n")
                        if msg.text == "/bye":
                            client.leaveGroup(msg.to)
                            JoinedGroups.remove(msg.to)
                        if "mk " in msg.text:
                            key = eval(msg.contentMetadata["MENTION"])
                            key["MENTIONEES"][0]["M"]
                            targets = []
                            for x in key["MENTIONEES"]:
                                targets.append(x["M"])
                            for target in targets:
                                if target in whiteListedMid:
                                    pass
                                else:
                                    try:
                                        client.kickoutFromGroup(msg.to,[target])
                                    except:
                                        pass
                        if msg.text == "/cancel":
                            group = client.getGroup(msg.to)
                            gMembMids = [contact.mid for contact in group.invitee]
                            for _mid in gMembMids:
                                client.cancelGroupInvitation(msg.to, [_mid])
                        if msg.text.startswith("/kick"):
                            str1 = find_between_r(msg.text, "/kick ", "")
                            if str1 not in whiteListedMid:
                                try:
                                    client.kickoutFromGroup(msg.to, [str1])
                                except Exception as e:
                                    print(e)
                                return
                else:
                    pass
            except:
                pass
        else:
            pass
    except Exception as error:
        print(error)
        print("\n\nRECEIVE_MESSAGE\n\n")
        return


oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP,
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION,
    OpType.NOTIFIED_UPDATE_GROUP: NOTIFIED_UPDATE_GROUP,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""


while True:
    oepoll.trace()
