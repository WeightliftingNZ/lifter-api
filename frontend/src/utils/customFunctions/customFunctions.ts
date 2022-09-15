/**
 * @param title - A title string (e.g. piped_title)
 * @returns Better looking title (e.g. Piped Title)
 */
export function titleMaker(title: string) {
  return title
    .replace("_", " ")
    .split(" ")
    .map((word) => {
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}

/**
 * @param hours - Hour of time (in 24 hr format)
 * @param minutes - Minute of time
 * @returns Return time in human reaable string
 */
export function timeConvert(hours: number, minutes: number) {
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

/**
 * @param isoDateTime
 * @returns Date time in human reaable format
 */
export function dateTimeConverter(
  isoDateTime: string,
  giveTime: boolean = true
) {
  const date = new Date(isoDateTime);
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
  const dateString = `${days[date.getDay()]}, ${date.getDate()} ${
    months[date.getMonth()]
  } ${date.getFullYear()}`;
  const timeString = `${timeConvert(date.getHours(), date.getMinutes())}`;

  if (giveTime) {
    return dateString.concat(" - ", timeString);
  }
  return dateString;
}
