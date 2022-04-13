// time converter, converting ISO into human reable time and date

function timeConvert(hours: number, minutes: number) {
  // hours and minutes in 24 hours time
  if (!(hours >= 0 && hours <= 23)) {
    throw new RangeError("Hours must between 0 and 23");
  }
  if (!(minutes >= 0 && minutes <= 59)) {
    throw new RangeError("Minutes must between 0 and 59");
  }

  let newHours: number = hours;
  let newMinutes: string = String(minutes);
  let format: string = "AM";

  if (hours === 0) {
    newHours = 12;
    format = "AM";
  }
  if (hours > 12) {
    newHours = hours - 12;
    format = "PM";
  }
  if (String(minutes).length === 1) {
    newMinutes = "0" + String(minutes);
  }

  return `${newHours}:${newMinutes} ${format}`;
}

function sessionDateTimeConvert(s: string) {
  // convert ISO datetime string into human readable date and time
  const date = new Date(s);
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  return `${days[date.getDay()]}, ${date.getDate()} ${
    months[date.getMonth()]
  } ${date.getFullYear()} - ${timeConvert(date.getHours(), date.getMinutes())}`;
}

export default sessionDateTimeConvert;
