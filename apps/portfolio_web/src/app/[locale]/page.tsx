import Image, { type ImageProps } from 'next/image'
import Link from 'next/link'
import clsx from 'clsx'
import { MessageCircle } from 'lucide-react'
import path from 'node:path'

import { Button } from '@/components/Button'
import { Container } from '@/components/Container'
import JsonDocumentRenderer from '@/components/renderer/JsonDocumentRenderer'
import { aboutContent } from '../../../content/about/content'
import {
  GitHubIcon,
  LinkedInIcon,
} from '@/components/SocialIcons'
import logoAnimaginary from '@/images/logos/animaginary.svg'
import logoHelioStream from '@/images/logos/helio-stream.svg'
import logoPlanetaria from '@/images/logos/planetaria.svg'
import wechatQrCode from '@/images/wechat_qrcode.jpg'
import image1 from '@/images/photos/image-1.jpg'
import image2 from '@/images/photos/image-2.jpg'
import image3 from '@/images/photos/image-3.jpg'
import image4 from '@/images/photos/image-4.jpg'
import image5 from '@/images/photos/image-5.jpg'
import { isLocale, localizePath, type Locale } from '@/i18n'
import { notFound } from 'next/navigation'

function BriefcaseIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      {...props}
    >
      <path
        d="M2.75 9.75a3 3 0 0 1 3-3h12.5a3 3 0 0 1 3 3v8.5a3 3 0 0 1-3 3H5.75a3 3 0 0 1-3-3v-8.5Z"
        className="fill-zinc-100 stroke-zinc-400 dark:fill-zinc-100/10 dark:stroke-zinc-500"
      />
      <path
        d="M3 14.25h6.249c.484 0 .952-.002 1.316.319l.777.682a.996.996 0 0 0 1.316 0l.777-.682c.364-.32.832-.319 1.316-.319H21M8.75 6.5V4.75a2 2 0 0 1 2-2h2.5a2 2 0 0 1 2 2V6.5"
        className="stroke-zinc-400 dark:stroke-zinc-500"
      />
    </svg>
  )
}

function SocialLink({
  icon: Icon,
  ...props
}: React.ComponentPropsWithoutRef<typeof Link> & {
  icon: React.ComponentType<{ className?: string }>
}) {
  return (
    <Link className="group -m-1 p-1" {...props}>
      <Icon className="h-6 w-6 fill-zinc-500 transition group-hover:fill-zinc-600 dark:fill-zinc-400 dark:group-hover:fill-zinc-300" />
    </Link>
  )
}

function Newsletter({ content }: { content: (typeof aboutContent)[Locale] }) {
  return (
    <div
      className="rounded-2xl border border-zinc-100 p-6 dark:border-zinc-700/40"
    >
      <h2 className="flex text-sm font-semibold text-zinc-900 dark:text-zinc-100">
        <MessageCircle
          className="h-6 w-6 flex-none text-zinc-400 dark:text-zinc-500"
          strokeWidth={1.5}
        />
        <span className="ml-3">{content.contact.title}</span>
      </h2>
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
        {content.contact.description}
      </p>
      <div className="group relative mt-6">
        <Button type="button" variant="secondary" className="w-full">
          {content.contact.button}
        </Button>
        <div className="pointer-events-none absolute right-0 bottom-full z-20 mb-3 hidden rounded-2xl border border-zinc-200 bg-white p-3 shadow-xl group-hover:block group-focus-within:block dark:border-zinc-700 dark:bg-zinc-800">
          <Image
            src={wechatQrCode}
            alt=""
            width={180}
            height={180}
            className="h-44 w-44 rounded-lg object-cover"
          />
        </div>
      </div>
    </div>
  )
}

interface Role {
  title: string
  description: string
  logo: ImageProps['src']
  href: string
}

function Role({ role }: { role: Role }) {
  return (
    <li>
      <Link href={role.href} className="group flex gap-4">
        <div className="relative mt-1 flex h-10 w-10 flex-none items-center justify-center rounded-full shadow-md ring-1 shadow-zinc-800/5 ring-zinc-900/5 dark:border dark:border-zinc-700/50 dark:bg-zinc-800 dark:ring-0">
          <Image src={role.logo} alt="" className="h-7 w-7" unoptimized />
        </div>
        <div className="min-w-0 flex-auto">
          <div className="text-sm font-medium text-zinc-900 dark:text-zinc-100">{role.title}</div>
          <div className="text-xs text-zinc-500 dark:text-zinc-400">{role.description}</div>
        </div>
        <span className="ml-auto self-center text-zinc-400 transition group-hover:text-teal-500">→</span>
      </Link>
    </li>
  )
}

function Resume({
  content,
  locale,
  cvHref,
}: {
  content: (typeof aboutContent)[Locale]
  locale: Locale
  cvHref: string
}) {
  let resume: Array<Role> = [
    {
      ...content.featuredProjects.items.cvBase,
      logo: logoHelioStream,
      href: localizePath('/projects/cv-base', locale),
    },
    {
      ...content.featuredProjects.items.questionForge,
      logo: logoPlanetaria,
      href: localizePath('/projects/question-forge', locale),
    },
    {
      ...content.featuredProjects.items.decisionEngine,
      logo: logoAnimaginary,
      href: localizePath('/projects/decision-engine', locale),
    },
  ]

  return (
    <div className="rounded-2xl border border-zinc-100 p-6 dark:border-zinc-700/40">
      <h2 className="flex text-sm font-semibold text-zinc-900 dark:text-zinc-100">
        <BriefcaseIcon className="h-6 w-6 flex-none" />
        <span className="ml-3">{content.featuredProjects.title}</span>
      </h2>
      <ol className="mt-6 space-y-4">
        {resume.map((role, roleIndex) => (
          <Role key={roleIndex} role={role} />
        ))}
      </ol>
      <Button
        href={cvHref}
        target="_blank"
        rel="noopener noreferrer"
        variant="secondary"
        className="group mt-6 w-full"
      >
        {content.featuredProjects.viewCv}
      </Button>
    </div>
  )
}

function Photos() {
  let rotations = ['rotate-2', '-rotate-2', 'rotate-2', 'rotate-2', '-rotate-2']

  return (
    <div className="mt-16 sm:mt-20">
      <div className="-my-4 flex justify-center gap-5 overflow-hidden py-4 sm:gap-8">
        {[image1, image2, image3, image4, image5].map((image, imageIndex) => (
          <div
            key={image.src}
            className={clsx(
              'relative w-44 flex-none overflow-hidden rounded-xl bg-zinc-100 sm:w-72 sm:rounded-2xl dark:bg-zinc-800',
              rotations[imageIndex % rotations.length],
            )}
          >
            <div className="aspect-9/10">
              <Image
                src={image}
                alt=""
                sizes="(min-width: 640px) 18rem, 11rem"
                className="absolute inset-0 h-full w-full object-cover"
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

type HomePageProps = {
  params: Promise<{ locale: string }>
}

export default async function Home({ params }: HomePageProps) {
  const { locale: rawLocale } = await params
  if (!isLocale(rawLocale)) {
    notFound()
  }
  const locale: Locale = rawLocale
  const jsonPath = path.join(
    process.cwd(),
    'content/about',
    `${locale}.json`,
  )
  const content = aboutContent[locale]
  const cvHref = locale === 'zh' ? '/cv_zh.html' : '/cv_en.html'

  return (
    <>
      <Container className="mt-9">
        <div className="max-w-2xl">
          <h1 className="text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
            {content.hero.title}
          </h1>
          <p className="mt-6 text-base text-zinc-600 dark:text-zinc-400">
            {content.hero.description}
          </p>
          <div className="mt-6 flex gap-6">
            <SocialLink
              href="https://github.com/mnsinker"
              aria-label="GitHub"
              icon={GitHubIcon}
            />
            <SocialLink
              href="https://www.linkedin.com/in/mnsink/"
              aria-label="LinkedIn"
              icon={LinkedInIcon}
            />
          </div>
        </div>
      </Container>
      <Photos />
      <Container className="mt-24 md:mt-28">
        <div className="mx-auto grid max-w-xl grid-cols-1 gap-y-20 lg:max-w-none lg:grid-cols-2">
          <div className="flex flex-col">
            <JsonDocumentRenderer jsonPath={jsonPath} showToc={false} />
          </div>
          <div className="space-y-10 lg:pl-16 xl:pl-24">
            <Newsletter content={content} />
            <Resume content={content} locale={locale} cvHref={cvHref} />
          </div>
        </div>
      </Container>
    </>
  )
}
