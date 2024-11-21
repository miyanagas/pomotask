const timeFormat = (time) => {
  const hours = Math.floor(time / 60 / 60);
  const minutes = String(Math.floor(time / 60) % 60).padStart(2, "0");
  const seconds = String(time % 60).padStart(2, "0");
  if (hours === 0) {
    return `${minutes}:${seconds}`;
  }
  return `${hours}:${minutes}:${seconds}`;
};

export { timeFormat };
