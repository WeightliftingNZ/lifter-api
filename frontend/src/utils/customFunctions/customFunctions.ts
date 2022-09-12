export function titleMaker(title: string) {
  /* Turns titles into text (e.g. 'date_started' => 'Date Started')*/
  return title
    .replace("_", " ")
    .split(" ")
    .map((word) => {
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}
