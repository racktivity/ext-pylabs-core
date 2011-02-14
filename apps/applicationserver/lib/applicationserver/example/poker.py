# <License type="Sun Cloud BSD" version="2.2">
#
# Copyright (c) 2005-2009, Sun Microsystems, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Neither the name Sun Microsystems, Inc. nor the names of other
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SUN MICROSYSTEMS, INC. "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SUN MICROSYSTEMS, INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# </License>
 
import uuid

from applicationserver import expose, cronjob

class PokerService:
    def __init__(self, initial_credit):
        self.tables = dict()
        self.initial_credit = initial_credit

    @expose
    def create_table(self, users):
        table_id = str(uuid.uuid1())
        users = tuple(u.strip() for u in users.split(','))
        table = PokerTable(users, self.initial_credit)

        self.tables[table_id] = table

        return (table_id, table.users)

    @expose
    def bet(self, table_id, user, amount):
        return self.tables[table_id].bet(user, amount)

    @expose
    def fold(self, table_id, winner):
        return self.tables[table_id].fold(winner)

    @expose
    def remove_table(self, table_id):
        del self.tables[table_id]
        return True

    @cronjob(10)
    def raise_credit(self):
        for table in self.tables.itervalues():
            table.raise_credit(20)

class PokerTable:
    def __init__(self, users, credit):
        self.users = dict((name, credit) for name in users)
        self.bets = 0

    def bet(self, user, amount):
        user_amount = self.users[user]
        amount = int(amount)
        if amount > user_amount:
            raise RuntimeError('User %s needs more cash first' % user)

        user_amount -= amount

        self.users[user] = user_amount
        self.bets += amount

        return self.users

    def fold(self, winner):
        self.users[winner] += self.bets
        self.bets = 0

        return self.users

    def raise_credit(self, percentage):
        for user, credit in self.users.iteritems():
            new_credit = int((1.0 + (percentage / 100.0)) * float(credit))
            self.users[user] = new_credit