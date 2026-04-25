export type Service = {
  id: number;
  title: string;
  description: string;
  items: string[];
  icon?: string | null;
  order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type ExperienceStatus = "proximamente" | "cupos_abiertos" | "finalizada";

export type Experience = {
  id: number;
  title: string;
  slug: string;
  description: string;
  date: string;
  location: string;
  capacity: number;
  available_spots: number;
  status: ExperienceStatus;
  cover_image?: string | null;
  gallery_images: string[];
  whatsapp_message?: string | null;
  is_published: boolean;
  created_at: string;
  updated_at: string;
};

export type BlogPost = {
  id: number;
  title: string;
  slug?: string | null;
  excerpt: string;
  content: string;
  category: string;
  cover_image?: string | null;
  is_published: boolean;
  published_at?: string | null;
  created_at: string;
  updated_at: string;
};

export type Testimonial = {
  id: number;
  name: string;
  text: string;
  service_type: string;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
};

export type ContactMessage = {
  id: number;
  full_name: string;
  email: string;
  phone?: string | null;
  reason: string;
  message: string;
  is_read: boolean;
  created_at: string;
};

export type SiteSetting = {
  id: number;
  key: string;
  value: string;
  updated_at: string;
};

export type AuthUser = {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
  user: AuthUser;
};

export type ContactPayload = {
  full_name: string;
  email: string;
  phone?: string;
  reason: string;
  message: string;
};

export type ExperiencePayload = Omit<
  Experience,
  "id" | "created_at" | "updated_at" | "slug"
> & {
  slug?: string;
};

export type BlogPayload = Omit<BlogPost, "id" | "created_at" | "updated_at">;

export type ServicePayload = Omit<Service, "id" | "created_at" | "updated_at">;

export type ContactUpdatePayload = Partial<
  Pick<ContactMessage, "full_name" | "email" | "phone" | "reason" | "message" | "is_read">
>;

export type SiteSettingsMap = Record<string, string>;

export type TestimonialPayload = Omit<
  Testimonial,
  "id" | "created_at" | "updated_at"
>;

export type SiteSettingPayload = Omit<SiteSetting, "id" | "updated_at">;
