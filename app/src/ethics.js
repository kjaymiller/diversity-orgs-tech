import React from "react";

export default function Ethics() {
  return (
    <div className="container mx-auto">
      <h1 className="text-5xl my-5 font-extralight">
        The Ethics Behind this Site
      </h1>
      <div className="mt-5 w-1/2">
        <h2 className="text-4xl my-5">
          Representation{" "}
          <span className="font-black text-indigo-500">Matters</span>
        </h2>
        <p>
          The goal of this app is to encourage folks from under-represented
          groups to get involved in their tech community of choice. There are
          many wonderful groups that advocate for representation and provide
          many resources to folks that identify as a member or ally of the
          groups they serve.
        </p>
        <h2 className="text-4xl my-5">
          Representation at{" "}
          <span className="font-black text-indigo-500">No Cost</span>
        </h2>
        <p className="my-3">
          This project is not a money making effor, nor is it a information
          grab.
        </p>
        <p className="my-3">
          This site will be available for free as long as I (Jay Miller) can
          afford to keep it that way. You can help support that cause, but it is
          not required to use this site.
        </p>

        <p className="my-3">
          This site does not sell information to any of the groups listed and
          there is no way for groups to <em>buy</em> position on it.
        </p>
      </div>
      <h2 className="text-4xl my-5">
        Representation{" "}
        <span className="font-black text-indigo-500">Grows Contstantly</span>
      </h2>
      <p className="my-3">
        This is mostly a solo project by me (Jay Miller). Many of these groups
        are added based on discovery and each group is verified. That said the
        goal is to include as many groups as possible.{" "}
      </p>
      <h3>Here are some representation segments that I'm covering:</h3>
      <ul class="my-2">
        <li>Asian American Pacific Islander</li>
        <li>Black/Indegenious People of Color</li>
        <li>Folks Experiencing Homelessness/Refugee Status</li>
        <li>Previously Incarcerated</li>
        <li>LGBTQIA+</li>
        <li>Latinx</li>
        <li>Members of a Minority Religious Group</li>
        <li>Women in Tech</li>
      </ul>
      <p className="my-3">
        If there is a group missing, apologies. Feel free to let us know using
        the chat icon on any page.
      </p>

      <h2 className="text-4xl my-5">
        Representation has{" "}
        <span className="uppercase text-red-600 font-black">no room </span> for
        Hatred
      </h2>
      <p className="my-3">
        This site will not support any organization with verified ties to
        racism, sexism, or supremacy{" "}
        <span className="font-bold uppercase">of any kind</span>.
      </p>
      <p className="my-3">
        If you see something that you are uncomfortable with I encourage you to
        use the chat form available on every page.
      </p>
    </div>
  );
}
