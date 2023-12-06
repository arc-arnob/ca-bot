package furhatos.app.skill.flow.main

import furhatos.app.skill.flow.Parent
import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.onResponse
import furhatos.flow.kotlin.state
import furhatos.gestures.Gestures
import furhatos.nlu.common.Greeting
import furhatos.nlu.common.Maybe
import furhatos.nlu.common.No
import furhatos.nlu.common.Yes

val Greeting: State = state(Parent) {
    onEntry {
        /** Greet the user **/
        furhat.say {
            random {
                +"Hello there. "
                +"Hi there! "
                +"Hello! "
            }
            +Gestures.BigSmile
        }
        furhat.ask("Should I say Hello World?")
        furhat.listen()
    }

    onResponse<Greeting> {
        val canIAskYouSomething = furhat.askYN("Can I ask you something?")
        if (canIAskYouSomething) {
            goto(Asking)
        } else {
            furhat.say("Sorry to bother you. ")
            furhat.gesture(Gestures.Thoughtful)
            furhat.stopGestures()
        }
    }

    onResponse<Yes> {
        furhat.say("Hello World! ")
        furhat.listen()
    }

    onResponse<No> {
        furhat.say("Ok.")
    }

    onResponse<Maybe> {
        furhat.say("Okay Ill try, Hello world, haha")
    }

}

