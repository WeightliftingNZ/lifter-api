/** @format */

import moment from "moment";

/**
 * Turn a date range into something better readable.
 * @param dateStart - Date start, preferred format 'YYYY-MM-DD'
 * @param dateEnd - Date end, same preferred format as date start
 */
export function dateRangeProvider(dateStart: string, dateEnd: string) {
  const yearDelta = moment(dateEnd).year() - moment(dateStart).year();
  const monthDelta = moment(dateEnd).month() - moment(dateStart).month();
  const dateDelta = moment(dateEnd).date() - moment(dateStart).date();

  if (yearDelta !== 0) {
    return `${moment(dateStart).format("ddd, Do MMM YYYY")} - ${moment(
      dateEnd
    ).format("ddd, Do MMM YYYY")}`;
  } else if (monthDelta !== 0) {
    return `${moment(dateStart).format("ddd, Do MMM")} - ${moment(
      dateEnd
    ).format("ddd, Do MMM YYYY")}`;
  } else if (dateDelta !== 0) {
    return `${moment(dateStart).format("ddd, Do")} - ${moment(dateEnd).format(
      "ddd, Do MMM YYYY"
    )}`;
  } else {
    return `${moment(dateStart).format("ddd, Do MMM YYYY")}`;
  }
}

/**
 * @format
 * @param weightCategory - Weight category (e.g M94)
 * @returns Human readable weight category
 */
export function printWeightCategories(weightCategory: string) {
  return `${weightCategory.replace("W", "Women's ").replace("M", "Men's ")} kg`;
}
