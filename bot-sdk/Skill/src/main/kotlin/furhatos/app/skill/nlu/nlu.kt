package furhatos.app.skill.nlu

import furhatos.nlu.*
import furhatos.nlu.common.PersonName
import furhatos.util.Language


class Fun: Intent(){
    override fun getExamples(lang: Language): List<String> {
        return listOf("That's funny?",
            "Haha",
            "Cool")
    }
}

class ProvideName(var name : PersonName? = null):Intent(){
    override fun getExamples(lang: Language): List<String> {
        return listOf("@name", "My @name is", "I am @name")
    }
}
