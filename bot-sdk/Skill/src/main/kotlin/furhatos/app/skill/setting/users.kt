package furhatos.app.skill.setting

import furhatos.records.User
import furhatos.flow.kotlin.UserDataDelegate


var User.likeRobots : Boolean? by UserDataDelegate()