import { createEvents } from 'ics'
import { undefinedExamDate } from './constants'

function getIcsStream(bucket: CourseEntry[]) {
    const eventDetails = bucket
        .filter(course => course.exam_d != undefinedExamDate)
        .map(course => { 
            const startDate = examStartDateUtc(course)
            const startDateArr = [startDate.getFullYear(), startDate.getMonth() + 1, startDate.getDate(), startDate.getHours(), startDate.getMinutes()]
            return {
                title: course.course_num,
                start: startDateArr as [number, number, number, number, number],
                duration: { hours: 2, minutes: 30 },
            }
        })

    const { error, value } = createEvents(eventDetails)
    if (error) console.log(error)

    console.log(value)
    
    return value || ""
}

function examStartDateUtc(course: CourseEntry): Date {
    const thaiDate = new Date(course.exam_d)
    const [h, m] = examStartTime(course)

    thaiDate.setHours(h);
    thaiDate.setMinutes(m);

    var now_utc = Date.UTC(thaiDate.getUTCFullYear(), thaiDate.getUTCMonth(), thaiDate.getUTCDate(), thaiDate.getUTCHours(), thaiDate.getUTCMinutes())

    return new Date(now_utc)
}

function examStartTime(course: CourseEntry) {
    switch (course.exam_t) {
        case "A": return [9, 30]
        case "B": return [14, 0]
        case "C": return [17, 0]
    }
}


export { getIcsStream }