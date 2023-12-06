package furhatos.app.skill.flow.main

import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.*
import furhatos.nlu.common.DontKnow
import furhatos.nlu.common.Maybe
import furhatos.nlu.common.No
import furhatos.nlu.common.Yes

val Asking:State = state(){
    onEntry {
        furhat.ask{
            +"Do You like Robots"
        }
    }
    onResponse<Yes> {
        furhat.say("How Nice")
    }
    onResponse<No> {
        furhat.say("Aww that's a shame")
    }

    onResponse<DontKnow> {
        furhat.say("Hmm That's Okay")
    }

    onResponse<Maybe> {
        furhat.say("I'm Going to tell you about it.")
    }

}