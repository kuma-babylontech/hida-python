export interface SlideMetadata {
  id: string;
  title: string;
  date: string;
  description: string;
  tags: string[];
  author?: string;
  thumbnail?: string;
}

export interface SlideData extends SlideMetadata {
  content: string;
}
